from __future__ import annotations

from typing import TYPE_CHECKING

from httpx import URL
from slugify import slugify
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schemas.atoms.life_status_enum import LifeStatus

from ._base import Base

if TYPE_CHECKING:
    from .deployed_model import DeployedModel
    from .model_interface_config import ModelInterfaceConfig


class ModelInterface(Base):
    __tablename__ = "model_interface"

    id: Mapped[int] = mapped_column(primary_key=True)
    """Unique identifier of the model interface."""
    friendly_name: Mapped[str] = mapped_column(String(100), nullable=False)
    """Friendly name of the model interface."""
    slug: Mapped[str] = mapped_column(String(100), nullable=True)
    """Another unique identifier of the model interface."""

    deployed_models: Mapped[list[DeployedModel]] = relationship(
        "DeployedModel", back_populates="model_interface"
    )
    configs: Mapped[list[ModelInterfaceConfig]] = relationship(
        "ModelInterfaceConfig", back_populates="model_interface"
    )
    last_config = relationship(
        "ModelInterfaceConfig",
        primaryjoin="ModelInterface.id==foreign(ModelInterfaceConfig.model_interface_id)",
        order_by="desc(ModelInterfaceConfig.id)",
        uselist=False,
    )

    deployed_url: Mapped[URL] = mapped_column(String(2000), nullable=True)
    """URL of the model interface. If None, the model interface is not deployed."""

    life_status: Mapped[LifeStatus] = mapped_column(nullable=False, default=LifeStatus.PENDING)
    """Current status of the model interface."""

    def compute_slug(self):
        self.slug = slugify(str(self.id) + "-" + self.friendly_name, max_length=100)
