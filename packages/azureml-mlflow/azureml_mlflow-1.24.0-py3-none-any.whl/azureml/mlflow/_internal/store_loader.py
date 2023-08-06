# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
from six.moves.urllib import parse

from azureml.core import Run

from .store import AzureMLRestStore

from .model_registry import AzureMLflowModelRegistry
from azureml.exceptions import RunEnvironmentException

from .utils import (get_service_context_from_tracking_url_default_auth,
                    _IS_REMOTE,
                    _TRUE_QUERY_VALUE)

logger = logging.getLogger(__name__)


class _AzureMLStoreLoader(object):
    """
    _AzureMLStoreLoader loads an AzureMLStore from 3 supported scenarios.

    1, new tracking_uri without is remote set to True. A store is created from the uri
    2, is remote set to true in a workspace tracking uri. Loads the
       store information from the current Run context and sets the experiment and ActiveRun.
    3, a cached result of option 1 or 2, this cache is relative to the netloc + path of the tracking_uri
    """

    _azure_uri_to_tracking_store = {}
    _azure_uri_to_model_registry_store = {}

    @classmethod
    def _load_azureml_tracking_store(cls, store_uri):
        return cls._load_azureml_store(store_uri, AzureMLRestStore, cls._azure_uri_to_tracking_store)

    @classmethod
    def _load_azureml_model_registry_store(cls, store_uri):
        return cls._load_azureml_store(store_uri, AzureMLflowModelRegistry, cls._azure_uri_to_model_registry_store)

    @classmethod
    def _load_azureml_store(cls, store_uri, store_object, cache_dict):
        import mlflow
        from mlflow.exceptions import MlflowException
        parsed_url = parse.urlparse(store_uri)
        queries = dict(parse.parse_qsl(parsed_url.query))
        # cache the Azure workspace object
        cache_key = store_uri.split("?")[0]
        if cache_key in cache_dict:
            return cache_dict[cache_key]
        elif _IS_REMOTE in queries and queries[_IS_REMOTE] == _TRUE_QUERY_VALUE:
            try:
                run = Run.get_context()
            except RunEnvironmentException:
                raise MlflowException(
                    "AzureMlflow tracking URI was set to remote but there was a failure in loading the run.")
            else:
                logger.debug("Creating a new {} for a remote run".format(store_object.__name__))
                amlflow_store = store_object(service_context=run.experiment.workspace.service_context)

                cache_dict[cache_key] = amlflow_store
                logger.debug("Setting Mlflow experiment with {}".format(run.experiment.name))
                mlflow.set_experiment(run.experiment.name)
        else:
            service_context = get_service_context_from_tracking_url_default_auth(parsed_url)
            logger.debug("Creating a new {} for a local run".format(store_object.__name__))
            cache_dict[cache_key] = store_object(service_context=service_context)

        return cache_dict[cache_key]

    @classmethod
    def _add_azureml_tracking_store(cls, store_uri, workspace):
        return cls._add_azureml_store(store_uri,
                                      AzureMLRestStore,
                                      cls._azure_uri_to_tracking_store,
                                      workspace)

    @classmethod
    def _add_azureml_model_registry_store(cls, store_uri, workspace):
        return cls._add_azureml_store(store_uri,
                                      AzureMLflowModelRegistry,
                                      cls._azure_uri_to_model_registry_store,
                                      workspace)

    @classmethod
    def _add_azureml_store(cls, store_uri, store_object, cache_dict, workspace):
        # cache the Azure workspace object
        cache_key = store_uri.split("?")[0]
        if cache_key in cache_dict:
            logger.debug("Loading an existing {} from the _AzureMLStoreLoader cache".format(store_object.__name__))
            return cache_dict[cache_key]
        else:
            cache_dict[cache_key] = store_object(service_context=workspace.service_context)
