from __future__ import annotations

from typing import Any


def build_vehicle_name(vehicle: dict[str, Any]) -> str:
    """Create a readable vehicle name."""
    year = vehicle.get("year")
    make = vehicle.get("make", "")
    model = vehicle.get("model", "")

    parts = [str(year) if year else None, make, model]
    name = " ".join(p for p in parts if p)

    return name or f"Vehicle {vehicle['id']}"
