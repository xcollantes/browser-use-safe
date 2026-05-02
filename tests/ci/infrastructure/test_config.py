"""Tests for lazy loading configuration system."""

import os

from browser_use.config import CONFIG


class TestLazyConfig:
	"""Test lazy loading of environment variables through CONFIG object."""

	def test_config_reads_env_vars_lazily(self):
		"""Test that CONFIG reads environment variables each time they're accessed."""
		# Set an env var
		original_value = os.environ.get('BROWSER_USE_LOGGING_LEVEL', '')
		try:
			os.environ['BROWSER_USE_LOGGING_LEVEL'] = 'debug'
			assert CONFIG.BROWSER_USE_LOGGING_LEVEL == 'debug'

			# Change the env var
			os.environ['BROWSER_USE_LOGGING_LEVEL'] = 'info'
			assert CONFIG.BROWSER_USE_LOGGING_LEVEL == 'info'

			# Delete the env var to test default
			del os.environ['BROWSER_USE_LOGGING_LEVEL']
			assert CONFIG.BROWSER_USE_LOGGING_LEVEL == 'info'  # default value
		finally:
			# Restore original value
			if original_value:
				os.environ['BROWSER_USE_LOGGING_LEVEL'] = original_value
			else:
				os.environ.pop('BROWSER_USE_LOGGING_LEVEL', None)

	def test_telemetry_is_hard_disabled(self):
		"""ANONYMIZED_TELEMETRY is permanently False in this fork regardless of env var."""
		original_value = os.environ.get('ANONYMIZED_TELEMETRY', '')
		try:
			for any_val in ['true', 'True', 'TRUE', 'yes', '1', 'false', '0', '']:
				os.environ['ANONYMIZED_TELEMETRY'] = any_val
				assert CONFIG.ANONYMIZED_TELEMETRY is False, f'Telemetry must stay disabled, got True for {any_val!r}'
		finally:
			if original_value:
				os.environ['ANONYMIZED_TELEMETRY'] = original_value
			else:
				os.environ.pop('ANONYMIZED_TELEMETRY', None)

	def test_api_keys_lazy_loading(self):
		"""Test API keys are loaded lazily."""
		original_value = os.environ.get('OPENAI_API_KEY', '')
		try:
			# Test empty default
			os.environ.pop('OPENAI_API_KEY', None)
			assert CONFIG.OPENAI_API_KEY == ''

			# Set a value
			os.environ['OPENAI_API_KEY'] = 'test-key-123'
			assert CONFIG.OPENAI_API_KEY == 'test-key-123'

			# Change the value
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
			# Test custom path
			test_path = '/tmp/test-cache'
			os.environ['XDG_CACHE_HOME'] = test_path
			# Use Path().resolve() to handle symlinks (e.g., /tmp -> /private/tmp on macOS)
			from pathlib import Path

			assert CONFIG.XDG_CACHE_HOME == Path(test_path).resolve()

			# Test default path expansion
			os.environ.pop('XDG_CACHE_HOME', None)
			assert '/.cache' in str(CONFIG.XDG_CACHE_HOME)
		finally:
			if original_value:
				os.environ['XDG_CACHE_HOME'] = original_value
			else:
				os.environ.pop('XDG_CACHE_HOME', None)

	def test_cloud_sync_is_hard_disabled(self):
		"""BROWSER_USE_CLOUD_SYNC is permanently False in this fork regardless of env vars."""
		telemetry_original = os.environ.get('ANONYMIZED_TELEMETRY', '')
		sync_original = os.environ.get('BROWSER_USE_CLOUD_SYNC', '')
		version_original = os.environ.get('BROWSER_USE_VERSION_CHECK', '')
		try:
			os.environ['ANONYMIZED_TELEMETRY'] = 'true'
			os.environ['BROWSER_USE_CLOUD_SYNC'] = 'true'
			os.environ['BROWSER_USE_VERSION_CHECK'] = 'true'
			assert CONFIG.BROWSER_USE_CLOUD_SYNC is False
			assert CONFIG.BROWSER_USE_VERSION_CHECK is False
		finally:
			for key, val in (
				('ANONYMIZED_TELEMETRY', telemetry_original),
				('BROWSER_USE_CLOUD_SYNC', sync_original),
				('BROWSER_USE_VERSION_CHECK', version_original),
			):
				if val:
					os.environ[key] = val
				else:
					os.environ.pop(key, None)
