"""ChatBrowserUse - removed in this local-only fork.

The upstream version calls https://llm.api.browser-use.com for inference.
This fork does not support that endpoint.
"""


class ChatBrowserUse:
	"""Stub: ChatBrowserUse has been removed from this local-only fork."""

	def __init__(self, *args, **kwargs):
		raise NotImplementedError(
			'ChatBrowserUse has been removed from this local-only fork. '
			'Use ChatOpenAI, ChatGoogle, ChatAnthropic, or another local-compatible model instead.'
		)
