"""Disabled telemetry service.

This fork of browser-use never sends telemetry to any external service.
The original posthog-based implementation has been replaced with a no-op
shim so that:

  - calling code (`agent/service.py`, `tools/registry/service.py`, `cli.py`)
    keeps working without changes
  - no posthog client is ever instantiated
  - no event is ever sent off-host
  - no `device_id` file is ever created

The `ANONYMIZED_TELEMETRY` env var is ignored on purpose — there is no way
to re-enable telemetry from configuration. To restore upstream behaviour,
revert this file from git history.
"""

from browser_use.telemetry.views import BaseTelemetryEvent
from browser_use.utils import singleton


@singleton
class ProductTelemetry:
	"""No-op stand-in for the upstream posthog telemetry client."""

	UNKNOWN_USER_ID = 'UNKNOWN_USER_ID'
	_curr_user_id = 'UNKNOWN_USER_ID'

	def __init__(self) -> None:
		self._posthog_client = None
		self.debug_logging = False

	def capture(self, event: BaseTelemetryEvent) -> None:
		return None

	def _direct_capture(self, event: BaseTelemetryEvent) -> None:
		return None

	def flush(self) -> None:
		return None

	@property
	def user_id(self) -> str:
		return self.UNKNOWN_USER_ID
