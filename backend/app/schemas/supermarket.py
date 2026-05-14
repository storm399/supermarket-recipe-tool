from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, ConfigDict


class SupermarketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    logo_url: Optional[str] = None
    active: bool = True
