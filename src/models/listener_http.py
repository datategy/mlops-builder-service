from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base
from .listener_interface import ListenerInterface


class ListenerHttp(ListenerInterface):
    __tablename__ = "listener_http"

    id: Mapped[int] = mapped_column(ForeignKey("listener.id"), primary_key=True)

    n_workers: Mapped[int] = mapped_column(nullable=False)
    n_threads: Mapped[int] = mapped_column(nullable=False)
    api_keys: Mapped[list["ApiKey"]] = relationship(back_populates="listener_http", lazy="joined")

    __mapper_args__ = {"polymorphic_identity": "http"}


class ApiKey(Base):
    __tablename__ = "api_key"

    id: Mapped[int] = mapped_column(primary_key=True)
    listener_http_id: Mapped[int] = mapped_column(ForeignKey("listener_http.id"))
    friendly_name: Mapped[str] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(nullable=False)
    can_create_new_api_keys: Mapped[bool] = mapped_column(nullable=False)
    store_inference_data: Mapped[bool] = mapped_column(nullable=False)
    listener_http: Mapped["ListenerHttp"] = relationship(back_populates="api_keys")
