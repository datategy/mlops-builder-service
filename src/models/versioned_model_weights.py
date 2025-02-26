from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base

if TYPE_CHECKING:
    from .deployment_version import DeploymentVersion
    from .model import Model


class VersionedModelWeight(Base):
    __tablename__ = "versioned_model_weight"

    id: Mapped[int] = mapped_column(primary_key=True)
    weight: Mapped[int] = mapped_column(nullable=False)
    deployment_version_id: Mapped[int] = mapped_column(ForeignKey("deployment_version.id"))
    deployment_version: Mapped[DeploymentVersion] = relationship("DeploymentVersion")
    model_id: Mapped[int] = mapped_column(ForeignKey("model.id"))
    model: Mapped[Model] = relationship("Model")
