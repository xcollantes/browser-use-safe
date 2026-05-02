"""Cloud browser views - stubbed out in this local-only fork."""

from pydantic import BaseModel, ConfigDict, Field


class CreateBrowserRequest(BaseModel):
	"""Stub: cloud browser support has been removed from this fork."""
	model_config = ConfigDict(extra='forbid', populate_by_name=True)


class CloudBrowserParams(BaseModel):
	"""Stub: cloud browser support has been removed from this fork."""
	model_config = ConfigDict(extra='forbid')


ProxyCountryCode = str
