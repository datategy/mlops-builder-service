from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base

if TYPE_CHECKING:
    from .deployed_model import DeployedModel


class DeployedModelWeight(Base):
    __tablename__ = "deployed_model_weight"

    id: Mapped[int] = mapped_column(primary_key=True)
    weight: Mapped[int] = mapped_column(nullable=False)
    deployed_model_id: Mapped[int] = mapped_column(ForeignKey("deployed_model.id"))
    deployed_model: Mapped[DeployedModel] = relationship("DeployedModel")
    created_on: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
