from __future__ import annotations

import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schemas.atoms.life_status_enum import LifeStatus

from ._base import Base

if TYPE_CHECKING:
    from .model_interface import ModelInterface
    from .versioned_model_weights import VersionedModelWeight


class Model(Base):
    __tablename__ = "model"

    id: Mapped[int] = mapped_column(primary_key=True)
    friendly_name: Mapped[str] = mapped_column(nullable=False)
    created_on: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    model_interface_id: Mapped[int] = mapped_column(ForeignKey("model_interface.id"))
    model_interface: Mapped[ModelInterface] = relationship(
        "ModelInterface", back_populates="models"
    )
    versioned_model_weight: Mapped[VersionedModelWeight] = relationship("VersionedModelWeight")

    artefacts_path: Mapped[Path] = mapped_column(nullable=False)

    life_status: Mapped[LifeStatus] = mapped_column(nullable=False, default=LifeStatus.PENDING)
