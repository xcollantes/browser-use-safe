"""Tripwire tests for the locked-down fork.

These tests assert that the modules upstream uses for telemetry, cloud
sync, version checks, cloud LLM, sandbox, and skills SDK have been
removed or stubbed in this fork. If somebody re-adds them these tests
will start failing and CI will flag it.
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


# --- New tripwires for the fully-local fork ---


def test_chat_browser_use_raises():
	"""ChatBrowserUse must raise NotImplementedError on instantiation."""
	from browser_use.llm.browser_use.chat import ChatBrowserUse

	with pytest.raises(NotImplementedError, match='removed from this local-only fork'):
		ChatBrowserUse()


def test_chat_browser_use_not_in_top_level_exports():
	"""ChatBrowserUse must not be in browser_use.__all__."""
	import browser_use

	assert 'ChatBrowserUse' not in browser_use.__all__


def test_sandbox_raises():
	"""sandbox() must raise NotImplementedError."""
	from browser_use.sandbox import sandbox

	with pytest.raises(NotImplementedError, match='removed from this fork'):
		sandbox()


def test_sandbox_not_in_top_level_exports():
	"""sandbox must not be in browser_use.__all__."""
	import browser_use

	assert 'sandbox' not in browser_use.__all__


def test_skill_service_raises():
	"""SkillService must raise NotImplementedError on instantiation."""
	from browser_use.skills.service import SkillService

	with pytest.raises(NotImplementedError, match='removed from this local-only fork'):
		SkillService()


def test_cloud_browser_client_create_raises():
	"""CloudBrowserClient.create_browser must raise CloudBrowserError."""
	from browser_use.browser.cloud.cloud import CloudBrowserClient, CloudBrowserError

	client = CloudBrowserClient()
	with pytest.raises(CloudBrowserError, match='removed from this fork'):
		import asyncio

		asyncio.get_event_loop().run_until_complete(client.create_browser())


def test_browser_use_sdk_not_in_dependencies():
	"""browser-use-sdk must not be importable as a runtime dependency."""
	with pytest.raises(ModuleNotFoundError):
		importlib.import_module('browser_use_sdk')


def test_no_default_pricing_url():
	"""TokenCost must not have a DEFAULT_PRICING_URL pointing to a remote endpoint."""
	from browser_use.tokens.service import TokenCost

	assert not hasattr(TokenCost, 'DEFAULT_PRICING_URL')
