# -*- coding: utf-8 -*-
"""
relay_commander.ld
~~~~~~~~~~~~~~~~~~

This module provides a wrapper for the LaunchDarkly API.

Reference API - https://pypi.org/project/launchdarkly-api/

.. versionchanged:: 0.0.12
    Refactor module to make it PEP-8 and PEP-484 compliant.
"""
import sys
import re
from util import LOG

import launchdarkly_api

class LaunchDarklyApi():
    """Wrapper for the LaunchDarkly API"""

    def __init__(
            self,
            api_key: str,
            project_key: str = None,
            environment_key: str = None
        ):
        """
        Instantiate a new LaunchDarklyApi instance.

        :param api_key: API Access Key for LaunchDarkly.
        :param project_key: Key for project.
        :param environment_key: Environment in which to \
            pull state from.
        """
        self.api_key = api_key
        self.project_key = project_key
        self.environment_key = environment_key

        # get new LD client
        configuration = launchdarkly_api.Configuration()
        configuration.api_key['Authorization'] = api_key
        self.client = launchdarkly_api.ProjectsApi(
            launchdarkly_api.ApiClient(configuration))
        self.feature = launchdarkly_api.FeatureFlagsApi(
            launchdarkly_api.ApiClient(configuration))
        self.custom_roles = launchdarkly_api.CustomRolesApi(
            launchdarkly_api.ApiClient(configuration))
        self.metric = launchdarkly_api.CustomerMetricsApi(
            launchdarkly_api.ApiClient(configuration))


    def get_custom_roles(self) -> dict:
        try:
            resp = self.custom_roles.get_custom_roles()
        except launchdarkly_api.rest.ApiException as ex:
            msg = "Unable to get environments."
            resp = "API response was {0} {1}.".format(ex.status, ex.reason)
            LOG.error("%s %s", msg, resp)
            sys.exit(1)

        roles = []

        for item in resp.items:
            if re.search("test", item.key):
                roles.append(item.key)

        return roles

    def get_flags(self, **kwargs) -> dict:
        try:
            resp = self.feature.get_feature_flags(**kwargs)
        except launchdarkly_api.rest.ApiException as ex:
            msg = "Unable to get environments."
            resp = "API response was {0} {1}.".format(ex.status, ex.reason)
            LOG.error("%s %s", msg, resp)
            sys.exit(1)

        flags = []

        for item in resp.items:
            flags.append(item.key)

        return flags

    def update_flag(self, state: str, feature_key: str) \
        -> launchdarkly_api.FeatureFlag:
        """
        Update the flag status for the specified feature flag.

        :param state: New feature flag state
        :param featureKey: Feature flag key

        :returns: FeatureFlag object.
        """
        build_env = "/environments/" + self.environment_key + "/on"
        patch_comment = [{"op": "replace", "path": build_env, "value": state}]

        try:
            resp = self.feature.patch_feature_flag(
                self.project_key, feature_key, patch_comment)
        except launchdarkly_api.rest.ApiException as ex:
            msg = "Unable to update flag."
            resp = "API response was {0} {1}.".format(ex.status, ex.reason)
            LOG.error("%s %s", msg, resp)
            sys.exit(1)

        return resp

    def delete_flag(self, feature_flag: str, project_key: str):
        try:
            resp = self.feature.delete_feature_flag(project_key, feature_flag)
        except launchdarkly_api.rest.ApiException as ex:
            msg = "Unable to delete flag."
            resp = "API response was {0} {1}.".format(ex.status, ex.reason)
            LOG.error("%s %s", msg, resp)
            sys.exit(1)

        return resp
