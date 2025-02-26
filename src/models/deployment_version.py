from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schemas.atoms.multi_model_mode_enum import MultiModelMode

from ._base import Base

if TYPE_CHECKING:
    from .model_interface import ModelInterface
    from .versioned_model_weights import VersionedModelWeight


class DeploymentVersion(Base):
    __tablename__ = "deployment_version"

    id: Mapped[int] = mapped_column(primary_key=True)
    model_interface_id: Mapped[int] = mapped_column(ForeignKey("model_interface.id"))
    model_interface: Mapped[ModelInterface] = relationship("ModelInterface")
    versioned_model_weights: Mapped[list[VersionedModelWeight]] = relationship(
        "VersionedModelWeight"
    )
    multi_model_mode: Mapped[MultiModelMode] = mapped_column(nullable=False)
    created_on: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
