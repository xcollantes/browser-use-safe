"""Tests for lazy loading configuration system."""

import os
from pathlib import Path

import pytest

from browser_use.config import CONFIG


class TestLazyConfig:
	"""Test lazy loading of environment variables through CONFIG object."""

	def test_config_reads_env_vars_lazily(self):
		"""Test that CONFIG reads environment variables each time they're accessed."""
		original_value = os.environ.get('BROWSER_USE_LOGGING_LEVEL', '')
		try:
			os.environ['BROWSER_USE_LOGGING_LEVEL'] = 'debug'
			assert CONFIG.BROWSER_USE_LOGGING_LEVEL == 'debug'

			os.environ['BROWSER_USE_LOGGING_LEVEL'] = 'info'
			assert CONFIG.BROWSER_USE_LOGGING_LEVEL == 'info'

			del os.environ['BROWSER_USE_LOGGING_LEVEL']
			assert CONFIG.BROWSER_USE_LOGGING_LEVEL == 'info'
		finally:
			if original_value:
				os.environ['BROWSER_USE_LOGGING_LEVEL'] = original_value
			else:
				os.environ.pop('BROWSER_USE_LOGGING_LEVEL', None)

	def test_api_keys_lazy_loading(self):
		"""Test API keys are loaded lazily."""
		original_value = os.environ.get('OPENAI_API_KEY', '')
		try:
			os.environ.pop('OPENAI_API_KEY', None)
			assert CONFIG.OPENAI_API_KEY == ''

			os.environ['OPENAI_API_KEY'] = 'test-key-123'
			assert CONFIG.OPENAI_API_KEY == 'test-key-123'

			os.environ['OPENAI_API_KEY'] = 'new-key-456'
			assert CONFIG.OPENAI_API_KEY == 'new-key-456'
		finally:
			if original_value:
				os.environ['OPENAI_API_KEY'] = original_value
			else:
				os.environ.pop('OPENAI_API_KEY', None)

	def test_path_configuration(self):
		"""Test path configuration variables."""
		original_value = os.environ.get('XDG_CACHE_HOME', '')
		try:
			test_path = '/tmp/test-cache'
			os.environ['XDG_CACHE_HOME'] = test_path
			assert CONFIG.XDG_CACHE_HOME == Path(test_path).resolve()

			os.environ.pop('XDG_CACHE_HOME', None)
			assert '/.cache' in str(CONFIG.XDG_CACHE_HOME)
		finally:
			if original_value:
				os.environ['XDG_CACHE_HOME'] = original_value
			else:
				os.environ.pop('XDG_CACHE_HOME', None)

	@pytest.mark.parametrize(
		'attr_name',
		[
			'ANONYMIZED_TELEMETRY',
			'BROWSER_USE_CLOUD_SYNC',
			'BROWSER_USE_CLOUD_API_URL',
			'BROWSER_USE_CLOUD_UI_URL',
			'BROWSER_USE_MODEL_PRICING_URL',
			'BROWSER_USE_VERSION_CHECK',
		],
	)
	def test_cloud_and_telemetry_keys_are_gone(self, attr_name):
		"""Cloud-sync and telemetry config keys must not exist on CONFIG in this fork."""
		with pytest.raises(AttributeError):
			getattr(CONFIG, attr_name)
