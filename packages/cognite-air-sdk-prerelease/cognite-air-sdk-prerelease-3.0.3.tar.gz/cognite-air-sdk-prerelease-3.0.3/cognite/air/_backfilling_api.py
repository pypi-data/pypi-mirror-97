import sys
import warnings
from contextlib import contextmanager

from cognite.air._api import AIRClientError, BaseAPIClient
from cognite.air.constants import (
    AIR_META_BACKFILL_COMPLETE,
    AIR_META_BACKFILL_LOCK,
    AIR_META_BACKFILL_LOCK_MAX_LOCK_TIME,
    AIR_META_BACKFILL_LOCK_SET_TIME_UNIX,
    AIR_META_BACKFILLED_UNTIL,
)
from cognite.air.ts_utils import current_time_in_ms
from cognite.air.utils import is_string_truthy
from cognite.client.data_classes import Asset, AssetUpdate


class NoBackfillAPI:
    @property
    def in_progress(self):
        return False

    def __getattr__(self, attr):
        raise AttributeError(
            f"Can't call backfilling endpoint after it is done! Failed when trying to get/call '{attr}'!"
        )


class AIRBackfillingAPI(BaseAPIClient):
    def __init__(self, config, backfill_asset):
        super().__init__(config)
        if not isinstance(backfill_asset, Asset):
            raise AIRClientError(
                f"Could not find the required backfilling asset! Expected {Asset}, not {type(backfill_asset)}"
            )
        self._backfill_asset = backfill_asset
        self._meta = self._backfill_asset.metadata

    @property
    def in_progress(self):
        return not is_string_truthy(self._meta[AIR_META_BACKFILL_COMPLETE])

    @property
    def latest_timestamp(self):
        backfilled_until = self._meta.get(AIR_META_BACKFILLED_UNTIL)
        if backfilled_until:
            return int(backfilled_until)

    @contextmanager
    def acquire_lock(self, system_exit_if_locked=True):
        """
        Usage:
        with air_client.backfilling.acquire_lock():
            my_code_that_must_run_serially()

        If a lock can not be acquired, the function will raise SystemExit.
        This can be ignored by passing 'system_exit_if_locked=False' (not recommended!)

        Warnings:
            Using LOCKS in AIR (airlocks, eh..) is still highly experimental
            and to be used at your own risk!
        """
        lock = self._meta.get(AIR_META_BACKFILL_LOCK, "False")
        lock_ts = int(self._meta.get(AIR_META_BACKFILL_LOCK_SET_TIME_UNIX, "0"))

        if not is_string_truthy(lock):  # If unset, immediately set
            self._set_lock()
        else:
            if current_time_in_ms() > lock_ts + AIR_META_BACKFILL_LOCK_MAX_LOCK_TIME:
                # Previous lock is ignored because of reaching timeout:
                self._set_lock()
            else:
                if system_exit_if_locked:
                    # Another Cognite Function is currently running.
                    # We exit to avoid concurrency problems:
                    sys.exit(0)
                else:
                    warnings.warn("Ignoring AIR-lock at your own risk!!", UserWarning)
        try:
            yield
        finally:
            self._release_lock()

    def _set_lock(self):
        lock_dct = {
            AIR_META_BACKFILL_LOCK: "True",
            AIR_META_BACKFILL_LOCK_SET_TIME_UNIX: str(current_time_in_ms()),
        }
        self._meta.update(lock_dct)
        self.client.assets.update(AssetUpdate(external_id=self._backfill_asset.external_id).metadata.add(lock_dct))

    def _release_lock(self):
        release_dct = {AIR_META_BACKFILL_LOCK: "False"}
        self._meta.update(release_dct)
        self.client.assets.update(AssetUpdate(external_id=self._backfill_asset.external_id).metadata.add(release_dct))

    def update_latest_timestamp(self, ts: int):
        if not isinstance(ts, int):
            raise TypeError(f"Expected input '{ts}' to be of type 'int' not '{type(ts)}'")
        self._meta[AIR_META_BACKFILLED_UNTIL] = ts
        self.client.assets.update(self._backfill_asset)

    def mark_as_completed(self):
        self._meta[AIR_META_BACKFILL_COMPLETE] = "True"
        self.client.assets.update(self._backfill_asset)
