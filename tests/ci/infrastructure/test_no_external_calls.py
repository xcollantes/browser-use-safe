"""Tripwire tests for the locked-down fork.

These tests assert that the four most common outbound paths in upstream
browser-use are no-ops in this fork:

  - ProductTelemetry never instantiates a posthog client
  - CloudSync never reports as enabled
  - DeviceAuthClient never reports as authenticated and never persists state
  - check_latest_browser_use_version never returns a result
  - lmnr observability is forced off
  - default extensions never auto-download

If any of these assertions fail in CI, somebody has re-introduced an
unsanctioned external call and the change should be reverted.
"""

import os

import pytest

from browser_use.config import CONFIG


def test_telemetry_client_is_noop():
	from browser_use.telemetry.service import ProductTelemetry

	t = ProductTelemetry()
	assert t._posthog_client is None
	assert t.user_id == 'UNKNOWN_USER_ID'


def test_cloud_sync_is_disabled():
	from browser_use.sync.service import CloudSync

	cs = CloudSync()
	assert cs.enabled is False


def test_auth_client_never_authenticated_and_no_disk_writes(tmp_path, monkeypatch):
	monkeypatch.setenv('BROWSER_USE_CONFIG_DIR', str(tmp_path / 'browseruse'))
	from browser_use.sync.auth import DeviceAuthClient

	c = DeviceAuthClient()
	assert c.is_authenticated is False
	assert c.api_token is None
	assert c.get_headers() == {}
	# DeviceAuthClient must not persist a `device_id` file or `cloud_auth.json`.
	assert not (tmp_path / 'browseruse' / 'device_id').exists()
	assert not (tmp_path / 'browseruse' / 'cloud_auth.json').exists()


@pytest.mark.asyncio
async def test_version_check_returns_none():
	from browser_use.utils import check_latest_browser_use_version

	assert await check_latest_browser_use_version() is None


def test_lmnr_observability_is_off():
	from browser_use import observability

	assert observability.is_lmnr_available() is False


def test_extensions_off_by_default():
	original = os.environ.pop('BROWSER_USE_DISABLE_EXTENSIONS', None)
	try:
		from browser_use.browser.profile import _get_enable_default_extensions_default

		assert _get_enable_default_extensions_default() is False
	finally:
		if original is not None:
			os.environ['BROWSER_USE_DISABLE_EXTENSIONS'] = original


def test_config_kill_switch():
	assert CONFIG.ANONYMIZED_TELEMETRY is False
	assert CONFIG.BROWSER_USE_CLOUD_SYNC is False
	assert CONFIG.BROWSER_USE_VERSION_CHECK is False
