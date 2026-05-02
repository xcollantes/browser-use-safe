"""Cloud browser support removed in this local-only fork."""


class CloudBrowserError(Exception):
	"""Raised when a cloud browser operation fails."""
	pass


class CloudBrowserAuthError(CloudBrowserError):
	"""Raised when cloud browser authentication fails."""
	pass


class CloudBrowserClient:
	"""Stub: cloud browser support has been removed from this fork."""

	def __init__(self, *args, **kwargs):
		pass

	async def create_browser(self, *args, **kwargs):
		raise CloudBrowserError(
			'Cloud browser support has been removed from this fork. '
			'Use a local browser or provide your own cdp_url instead.'
		)
