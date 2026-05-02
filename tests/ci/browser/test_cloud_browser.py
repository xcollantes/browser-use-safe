"""Tests for cloud browser functionality."""

from unittest.mock import AsyncMock, patch

import pytest

from browser_use.browser.cloud.cloud import (
	CloudBrowserAuthError,
	CloudBrowserClient,
	CloudBrowserError,
)
from browser_use.browser.cloud.views import CreateBrowserRequest
from browser_use.browser.profile import BrowserProfile
from browser_use.browser.session import BrowserSession


class TestCloudBrowserClient:
	"""Test CloudBrowserClient class."""

	async def test_create_browser_success(self, monkeypatch):
		"""Test successful cloud browser creation."""

		monkeypatch.setenv('BROWSER_USE_API_KEY', 'test-token')

		mock_response_data = {
			'id': 'test-browser-id',
			'status': 'active',
			'liveUrl': 'https://live.browser-use.com?wss=test',
			'cdpUrl': 'wss://test.proxy.daytona.works',
			'timeoutAt': '2025-09-17T04:35:36.049892',
			'startedAt': '2025-09-17T03:35:36.049974',
			'finishedAt': None,
		}

		with patch('httpx.AsyncClient') as mock_client_class:
			mock_response = AsyncMock()
			mock_response.status_code = 201
			mock_response.is_success = True
			mock_response.json = lambda: mock_response_data

			mock_client = AsyncMock()
			mock_client.post.return_value = mock_response
			mock_client_class.return_value = mock_client

			client = CloudBrowserClient()
			client.client = mock_client

			result = await client.create_browser(CreateBrowserRequest())

			assert result.id == 'test-browser-id'
			assert result.status == 'active'
			assert result.cdpUrl == 'wss://test.proxy.daytona.works'

			mock_client.post.assert_called_once()
			call_args = mock_client.post.call_args
			assert call_args.kwargs['headers']['X-Browser-Use-API-Key'] == 'test-token'

	async def test_create_browser_auth_error(self, monkeypatch):
		"""Missing API key must surface as CloudBrowserAuthError."""

		monkeypatch.delenv('BROWSER_USE_API_KEY', raising=False)

		client = CloudBrowserClient()

		with pytest.raises(CloudBrowserAuthError) as exc_info:
			await client.create_browser(CreateBrowserRequest())

		assert 'BROWSER_USE_API_KEY is not set' in str(exc_info.value)

	async def test_create_browser_http_401(self, monkeypatch):
		"""Test cloud browser creation with HTTP 401 response."""

		monkeypatch.setenv('BROWSER_USE_API_KEY', 'test-token')

		with patch('httpx.AsyncClient') as mock_client_class:
			mock_response = AsyncMock()
			mock_response.status_code = 401
			mock_response.is_success = False

			mock_client = AsyncMock()
			mock_client.post.return_value = mock_response
			mock_client_class.return_value = mock_client

			client = CloudBrowserClient()
			client.client = mock_client

			with pytest.raises(CloudBrowserAuthError) as exc_info:
				await client.create_browser(CreateBrowserRequest())

			assert 'BROWSER_USE_API_KEY is invalid' in str(exc_info.value)

	async def test_stop_browser_success(self, monkeypatch):
		"""Test successful cloud browser session stop."""

		monkeypatch.setenv('BROWSER_USE_API_KEY', 'test-token')

		mock_response_data = {
			'id': 'test-browser-id',
			'status': 'stopped',
			'liveUrl': 'https://live.browser-use.com?wss=test',
			'cdpUrl': 'wss://test.proxy.daytona.works',
			'timeoutAt': '2025-09-17T04:35:36.049892',
			'startedAt': '2025-09-17T03:35:36.049974',
			'finishedAt': '2025-09-17T04:35:36.049892',
		}

		with patch('httpx.AsyncClient') as mock_client_class:
			mock_response = AsyncMock()
			mock_response.status_code = 200
			mock_response.is_success = True
			mock_response.json = lambda: mock_response_data

			mock_client = AsyncMock()
			mock_client.patch.return_value = mock_response
			mock_client_class.return_value = mock_client

			client = CloudBrowserClient()
			client.client = mock_client
			client.current_session_id = 'test-browser-id'

			result = await client.stop_browser()

			assert result.id == 'test-browser-id'
			assert result.status == 'stopped'
			assert result.finishedAt is not None

			mock_client.patch.assert_called_once()
			call_args = mock_client.patch.call_args
			assert 'test-browser-id' in call_args.args[0]
			assert call_args.kwargs['json'] == {'action': 'stop'}
			assert call_args.kwargs['headers']['X-Browser-Use-API-Key'] == 'test-token'

	async def test_stop_browser_session_not_found(self, monkeypatch):
		"""Test stopping a browser session that doesn't exist."""

		monkeypatch.setenv('BROWSER_USE_API_KEY', 'test-token')

		with patch('httpx.AsyncClient') as mock_client_class:
			mock_response = AsyncMock()
			mock_response.status_code = 404
			mock_response.is_success = False

			mock_client = AsyncMock()
			mock_client.patch.return_value = mock_response
			mock_client_class.return_value = mock_client

			client = CloudBrowserClient()
			client.client = mock_client

			with pytest.raises(CloudBrowserError) as exc_info:
				await client.stop_browser('nonexistent-session')

			assert 'not found' in str(exc_info.value)


class TestBrowserSessionCloudIntegration:
	"""Test BrowserSession integration with cloud browsers."""

	async def test_cloud_browser_profile_property(self):
		"""Test that cloud_browser property works correctly."""

		profile = BrowserProfile(use_cloud=True)
		session = BrowserSession(browser_profile=profile, cdp_url='ws://mock-url')

		assert session.cloud_browser is True
		assert session.browser_profile.use_cloud is True

	async def test_browser_session_cloud_browser_logic(self, monkeypatch):
		"""Test that cloud browser profile settings work correctly."""

		monkeypatch.setenv('BROWSER_USE_API_KEY', 'test-token')

		profile = BrowserProfile(use_cloud=True)
		assert profile.use_cloud is True

		session = BrowserSession(browser_profile=profile, cdp_url='ws://mock-url')
		assert session.cloud_browser is True
