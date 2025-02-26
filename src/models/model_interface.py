from __future__ import annotations

from typing import TYPE_CHECKING

from slugify import slugify
from sqlalchemy import JSON, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schemas.atoms.life_status_enum import LifeStatus

from ._base import Base

if TYPE_CHECKING:
    import datetime

    from httpx import URL

    from src.schemas.atoms.use_case_enum import UseCase

    from .deployment_version import DeploymentVersion
    from .listener_interface import ListenerInterface
    from .model import Model


class ModelInterface(Base):
    __tablename__ = "model_interface"

    id: Mapped[int] = mapped_column(primary_key=True)
    """Unique identifier of the model interface."""
    friendly_name: Mapped[str] = mapped_column(String(100), nullable=False)
    """Friendly name of the model interface."""
    slug: Mapped[str] = mapped_column(String(100), nullable=True)
    """Another unique identifier of the model interface."""
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    use_case: Mapped[UseCase] = mapped_column(nullable=False)
    feature_names: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    """Names of the features used by the models of this model interface."""
    target_names: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    """Names of the targets of the models of this model interface."""

    listener_id: Mapped[int] = mapped_column(ForeignKey("listener.id"))
    listener: Mapped[ListenerInterface] = relationship(lazy="joined")

    models: Mapped[list[Model]] = relationship("Model", back_populates="model_interface")

    deployment_versions: Mapped[list[DeploymentVersion]] = relationship("DeploymentVersion")

    url: Mapped[URL] = mapped_column(String(2000), nullable=True)
    """URL of the model interface. If None, the model interface is not deployed."""

    created_on: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    life_status: Mapped[LifeStatus] = mapped_column(nullable=False, default=LifeStatus.PENDING)
    """Current status of the model interface."""

    def compute_slug(self):
        self.slug = slugify(str(self.id) + "-" + self.friendly_name, max_length=100)
