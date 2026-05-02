"""Disabled OAuth2 device authorization client.

This fork of browser-use never contacts `api.browser-use.com` for OAuth.
The original `DeviceAuthClient` ran the OAuth2 device authorization grant
flow, persisted an API token to `~/.config/browseruse/cloud_auth.json`,
and used it to attach a `Bearer` header to cloud sync requests. That has
been removed; this module now provides a stub with the same public surface
so imports keep working without any network calls.

`get_or_create_device_id()` no longer touches disk so a stable persistent
identifier is never written. A fresh per-process UUID is returned instead.
"""

from datetime import datetime

from pydantic import BaseModel
from uuid_extensions import uuid7str

# Sentinel kept for compatibility with cloud event payload shapes.
TEMP_USER_ID = '99999999-9999-9999-9999-999999999999'


def get_or_create_device_id() -> str:
	"""Return a fresh per-process UUID — no on-disk persistence."""
	return uuid7str()


class CloudAuthConfig(BaseModel):
	api_token: str | None = None
	user_id: str | None = None
	authorized_at: datetime | None = None

	@classmethod
	def load_from_file(cls) -> 'CloudAuthConfig':
		return cls()

	def save_to_file(self) -> None:
		return None


class DeviceAuthClient:
	"""No-op stand-in for the upstream OAuth2 device-flow client."""

	def __init__(self, base_url: str | None = None, http_client=None):
		self.base_url = base_url or ''
		self.client_id = 'library'
		self.scope = 'read write'
		self.http_client = http_client
		self.temp_user_id = TEMP_USER_ID
		self.device_id = get_or_create_device_id()
		self.auth_config = CloudAuthConfig()

	@property
	def is_authenticated(self) -> bool:
		return False

	@property
	def api_token(self) -> str | None:
		return None

	@property
	def user_id(self) -> str:
		return self.temp_user_id

	async def start_device_authorization(self, agent_session_id: str | None = None) -> dict:
		raise RuntimeError('Cloud authentication is disabled in this fork')

	async def poll_for_token(self, device_code: str, interval: float = 3.0, timeout: float = 1800.0) -> dict | None:
		return None

	async def authenticate(self, agent_session_id: str | None = None, show_instructions: bool = True) -> bool:
		return False

	def get_headers(self) -> dict:
		return {}

	def clear_auth(self) -> None:
		self.auth_config = CloudAuthConfig()
