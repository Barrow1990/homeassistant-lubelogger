from __future__ import annotations

import asyncio
import aiohttp
import async_timeout
import logging

from typing import Any, Optional

_LOGGER = logging.getLogger(__name__)


class LubeLoggerApi:
    """Async API client for LubeLogger."""

    def __init__(self, base_url: str, username: Optional[str], password: Optional[str]):
        self._base_url = base_url.rstrip("/")
        self._username = username
        self._password = password
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Ensure we have a persistent aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        """Internal HTTP request helper."""
        url = f"{self._base_url}{path}"

        session = await self._get_session()

        # Clean headers safely
        raw_headers = kwargs.pop("headers", {}) or {}
        headers = {
            str(k): str(v)
            for k, v in raw_headers.items()
            if k is not None and v is not None
        }
        headers["Accept"] = "application/json"

        auth = None
        if self._username and self._password:
            auth = aiohttp.BasicAuth(self._username, self._password)

        try:
            async with async_timeout.timeout(20):
                async with session.request(
                    method,
                    url,
                    headers=headers,
                    auth=auth,
                    **kwargs,
                ) as resp:
                    if resp.status >= 400:
                        text = await resp.text()
                        raise RuntimeError(
                            f"LubeLogger API error {resp.status}: {text}"
                        )

                    if resp.content_type == "application/json":
                        return await resp.json()

                    return await resp.text()

        except asyncio.TimeoutError:
            raise
        except aiohttp.ClientError as err:
            raise

    # -------------------------------------------------------------------------
    # Public GET API methods
    # -------------------------------------------------------------------------

    async def get_vehicles(self) -> list[dict[str, Any]]:
        """Return all vehicles."""
        return await self._request("GET", "/api/vehicles")

    async def get_latest_odometer(self, vehicle_id: int) -> Optional[float]:
        """Return the latest odometer value for a vehicle."""
        value = await self._request(
            "GET",
            f"/api/vehicle/odometerrecords/latest?vehicleId={vehicle_id}",
        )

        # API guarantees this is an int, but we normalize to float
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    async def get_odometer_records(self, vehicle_id: int) -> list[dict[str, Any]]:
        """Return all odometer records for a vehicle."""
        records = await self._request(
            "GET",
            f"/api/vehicle/odometerrecords?vehicleId={vehicle_id}",
        )

        # Ensure it's always a list
        return records if isinstance(records, list) else []

    async def get_service_history(self, vehicle_id: int):
        """Return service history for a vehicle."""
        return await self._request("GET", f"/api/vehicles/{vehicle_id}/services")

    async def get_fuel_logs(self, vehicle_id: int):
        """Return fuel logs for a vehicle."""
        return await self._request("GET", f"/api/vehicles/{vehicle_id}/fuel")

    # -------------------------------------------------------------------------
    # Public ADD API methods
    # -------------------------------------------------------------------------

    async def add_odometer_entry(self, vehicle_id: int, value: float, date: str):
        """Add a new odometer entry."""
        payload = {
            "odometer": value,
            "date": date,
        }

        return await self._request(
            "POST",
            f"/api/vehicle/odometerrecords/add?vehicleId={vehicle_id}",
            json=payload,
        )

    async def add_service_record(self, vehicle_id: int, data: dict[str, Any]):
        """Add a new service record."""
        payload = data.copy()
        payload["vehicleId"] = vehicle_id

        return await self._request(
            "POST",
            "/api/vehicle/servicerecords",
            json=payload,
        )
