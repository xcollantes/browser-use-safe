"""Disabled cloud sync service.

This fork of browser-use never sends events to the Browser Use cloud.
The original implementation POSTed agent session, task, and step events
(including DOM state, screenshots, and goals) to `https://api.browser-use.com`.
That has been removed; this module now provides a stub with the same
public surface used by the rest of the codebase so imports and attribute
access keep working without any network calls.
"""

from bubus import BaseEvent

from browser_use.sync.auth import DeviceAuthClient


class CloudSync:
	"""No-op stand-in for the upstream cloud sync service."""

	def __init__(
		self,
		base_url: str | None = None,
		allow_session_events_for_auth: bool = False,
	):
		self.base_url = base_url or ''
		self.auth_client = DeviceAuthClient(base_url=self.base_url)
		self.session_id: str | None = None
		self.allow_session_events_for_auth = allow_session_events_for_auth
		self.auth_flow_active = False
		self.enabled = False

	async def handle_event(self, event: BaseEvent) -> None:
		return None

	async def _send_event(self, event: BaseEvent) -> None:
		return None

	def set_auth_flow_active(self) -> None:
		self.auth_flow_active = True

	async def authenticate(self, show_instructions: bool = True) -> bool:
		return False
