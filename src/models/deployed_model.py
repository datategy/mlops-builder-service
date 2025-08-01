from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schemas.atoms.life_status_enum import LifeStatus

from ._base import Base

if TYPE_CHECKING:
    from .deployed_model_weight import DeployedModelWeight
    from .model_interface import ModelInterface


class DeployedModel(Base):
    __tablename__ = "deployed_model"

    id: Mapped[int] = mapped_column(primary_key=True)

    model_interface_id: Mapped[int] = mapped_column(ForeignKey("model_interface.id"))
    model_interface: Mapped[ModelInterface] = relationship(
        "ModelInterface", back_populates="deployed_models"
    )
    deployed_model_weights: Mapped[list[DeployedModelWeight]] = relationship(
        "DeployedModelWeight", back_populates="deployed_model"
    )

    artefacts_folder: Mapped[Path] = mapped_column(nullable=False)

    life_status: Mapped[LifeStatus] = mapped_column(nullable=False, default=LifeStatus.PENDING)
