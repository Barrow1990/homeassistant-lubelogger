from __future__ import annotations

import aiohttp
import async_timeout
import asyncio
import logging
import time

_LOGGER = logging.getLogger(__name__)


class LubeLoggerApiBase:
    """Base class for all LubeLogger API endpoints with logging, error handling, and auth detection."""

    def __init__(self, base_url: str, username: str | None, password: str | None):
        self._base_url = base_url.rstrip("/")
        self._username = username
        self._password = password
        self._last_error: str | None = None

    async def _request(self, method: str, path: str, **kwargs):
        url = f"{self._base_url}{path}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        # Determine auth mode
        auth = None
        auth_mode = "none"

        if self._username:
            auth = aiohttp.BasicAuth(self._username, self._password or "")
            auth_mode = "basic"

        start = time.monotonic()

        try:
            async with async_timeout.timeout(20):
                async with aiohttp.ClientSession() as session:
                    async with session.request(
                        method,
                        url,
                        headers=headers,
                        auth=auth,
                        **kwargs,
                    ) as resp:

                        duration = round(time.monotonic() - start, 3)

                        # Log request summary
                        _LOGGER.debug(
                            "LubeLogger API %s %s (auth=%s) → %s in %ss",
                            method,
                            url,
                            auth_mode,
                            resp.status,
                            duration,
                        )

                        # Handle auth failures
                        if resp.status == 401:
                            self._last_error = "Authentication failed (401)"
                            _LOGGER.error("LubeLogger: Authentication failed (401)")
                            raise aiohttp.ClientResponseError(
                                resp.request_info,
                                resp.history,
                                status=401,
                                message="Authentication failed",
                            )

                        if resp.status == 403:
                            self._last_error = "Forbidden (403)"
                            _LOGGER.error("LubeLogger: Access forbidden (403)")
                            raise aiohttp.ClientResponseError(
                                resp.request_info,
                                resp.history,
                                status=403,
                                message="Forbidden",
                            )

                        resp.raise_for_status()

                        try:
                            return await resp.json()
                        except Exception:
                            text = await resp.text()
                            _LOGGER.error("LubeLogger: Invalid JSON response: %s", text)
                            raise

        except asyncio.TimeoutError:
            self._last_error = "Timeout"
            _LOGGER.error("LubeLogger: Request timed out (%s %s)", method, url)
            raise

        except aiohttp.ClientConnectorError as err:
            self._last_error = f"Connection error: {err}"
            _LOGGER.error("LubeLogger: Connection error: %s", err)
            raise

        except aiohttp.ClientResponseError as err:
            self._last_error = f"HTTP error {err.status}: {err.message}"
            _LOGGER.error("LubeLogger: HTTP error %s: %s", err.status, err.message)
            raise

        except Exception as err:
            self._last_error = f"Unexpected error: {err}"
            _LOGGER.exception("LubeLogger: Unexpected error")
            raise
