"""Tripwire tests for the locked-down fork.

These tests assert that the modules upstream uses for telemetry, cloud
sync, version checks, and tracing have been removed entirely from this
fork. If somebody re-adds them the imports below will start succeeding
and CI will flag it.
"""

import importlib

import pytest


@pytest.mark.parametrize(
	'module_name',
	[
		'browser_use.telemetry',
		'browser_use.telemetry.service',
		'browser_use.telemetry.views',
		'browser_use.sync',
		'browser_use.sync.auth',
		'browser_use.sync.service',
		'browser_use.init_cmd',
	],
)
def test_removed_modules_cannot_be_imported(module_name):
	with pytest.raises(ModuleNotFoundError):
		importlib.import_module(module_name)


def test_version_check_helper_is_gone():
	from browser_use import utils

	assert not hasattr(utils, 'check_latest_browser_use_version')


def test_observability_is_a_passthrough():
	"""@observe / @observe_debug must be pure pass-throughs (no lmnr import path)."""
	import browser_use.observability as observability

	assert not hasattr(observability, 'is_lmnr_available')
	assert not hasattr(observability, '_LMNR_AVAILABLE')

	called: list[int] = []

	@observability.observe(name='unit')
	def fn(x: int) -> int:
		called.append(x)
		return x + 1

	assert fn(3) == 4
	assert called == [3]


def test_extensions_off_by_default(monkeypatch):
	monkeypatch.delenv('BROWSER_USE_DISABLE_EXTENSIONS', raising=False)
	from browser_use.browser.profile import _get_enable_default_extensions_default

	assert _get_enable_default_extensions_default() is False


def test_config_does_not_expose_cloud_keys():
	from browser_use.config import CONFIG

	for attr in (
		'ANONYMIZED_TELEMETRY',
		'BROWSER_USE_CLOUD_SYNC',
		'BROWSER_USE_CLOUD_API_URL',
		'BROWSER_USE_CLOUD_UI_URL',
		'BROWSER_USE_MODEL_PRICING_URL',
		'BROWSER_USE_VERSION_CHECK',
	):
		with pytest.raises(AttributeError):
			getattr(CONFIG, attr)
