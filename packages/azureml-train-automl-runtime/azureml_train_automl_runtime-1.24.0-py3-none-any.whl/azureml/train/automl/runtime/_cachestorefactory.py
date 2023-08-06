# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Factory class that automatically selects the appropriate cache store."""
import logging
from typing import Optional

from azureml.automl.core.shared import logging_utilities
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.file_cache_store import FileCacheStore, _CacheConstants
from azureml.automl.runtime.shared.memory_cache_store import MemoryCacheStore
from azureml.data.azure_storage_datastore import AbstractAzureStorageDatastore
from azureml.train.automl.runtime._azurefilecachestore import AzureFileCacheStore

logger = logging.getLogger(__name__)


class CacheStoreFactory:

    @staticmethod
    def get_cache_store(temp_location: str,
                        run_target: str,
                        run_id: Optional[str],
                        data_store: Optional[AbstractAzureStorageDatastore] = None,
                        task_timeout: int = _CacheConstants.DEFAULT_TASK_TIMEOUT_SECONDS) -> CacheStore:
        """Get the cache store based on run type."""
        try:
            if run_id is None:
                return MemoryCacheStore()

            if data_store is not None and run_target is not "local":
                return AzureFileCacheStore(
                    path=run_id,
                    account_name=data_store.account_name,
                    account_key=data_store.account_key,
                    sas_token=data_store.sas_token,
                    endpoint_suffix=data_store.endpoint,
                    temp_location=temp_location,
                    task_timeout=task_timeout)

            return FileCacheStore(path=temp_location, task_timeout=task_timeout)
        except Exception as e:
            logger.warning("Cannot proceed with the Run {} without a valid storage for intermediate files. "
                           "Encountered an exception of type: {}".format(run_id, type(e)))
            raise
