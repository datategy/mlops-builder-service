from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base

if TYPE_CHECKING:
    from .model_interface import ModelInterface


class ModelInterfaceConfig(Base):
    __tablename__ = "model_interface_config"

    id: Mapped[int] = mapped_column(primary_key=True)
    """Unique identifier of the model interface config."""
    model_interface_id: Mapped[int] = mapped_column(ForeignKey("model_interface.id"))
    """Foreign key to the model interface."""
    model_interface: Mapped[ModelInterface] = relationship(
        "ModelInterface", back_populates="configs"
    )

    config: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    """Configuration of the model interface."""

    created_on: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
