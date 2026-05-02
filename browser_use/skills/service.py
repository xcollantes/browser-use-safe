"""Skills service - removed in this local-only fork.

The upstream version connects to the Browser Use cloud API via browser-use-sdk.
This fork does not support remote skills.
"""


class SkillService:
	"""Stub: skill service has been removed from this fork."""

	def __init__(self, *args, **kwargs):
		raise NotImplementedError(
			'SkillService has been removed from this local-only fork. '
			'It requires the browser-use-sdk which connects to Browser Use cloud APIs.'
		)
