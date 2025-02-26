from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .listener_interface import ListenerInterface


class ListenerBroker(ListenerInterface):
    __tablename__ = "listener_broker"

    id: Mapped[int] = mapped_column(ForeignKey("listener.id"), primary_key=True)

    listener_id: Mapped[int] = mapped_column(nullable=False)
    broker_host: Mapped[str] = mapped_column(nullable=False)
    broker_port: Mapped[int] = mapped_column(nullable=False)
    broker_username: Mapped[str] = mapped_column(nullable=False)
    broker_password: Mapped[str] = mapped_column(nullable=False)

    __mapper_args__ = {"polymorphic_identity": "broker"}
