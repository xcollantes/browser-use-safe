"""Observability decorator stubs.

The upstream version of this module wires `@observe` / `@observe_debug`
through the `lmnr` (Laminar) tracing SDK. This fork strips that out:
no telemetry, no span creation, no third-party imports. The decorators
keep the same call signature so existing call sites continue to work
unchanged, but they are pure pass-throughs.
"""

import asyncio
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])


def _passthrough(func: F) -> F:
	if asyncio.iscoroutinefunction(func):

		@wraps(func)
		async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
			return await func(*args, **kwargs)

		return cast(F, async_wrapper)

	@wraps(func)
	def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
		return func(*args, **kwargs)

	return cast(F, sync_wrapper)


def observe(*_args: Any, **_kwargs: Any) -> Callable[[F], F]:
	"""No-op replacement for the upstream lmnr `observe` decorator."""
	return _passthrough


def observe_debug(*_args: Any, **_kwargs: Any) -> Callable[[F], F]:
	"""No-op replacement for the upstream lmnr `observe_debug` decorator."""
	return _passthrough
