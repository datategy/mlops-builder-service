from sqlalchemy.orm import Mapped, mapped_column

from ._base import Base


class ListenerInterface(Base):
    __tablename__ = "listener"

    id: Mapped[int] = mapped_column(primary_key=True)
    discriminator: Mapped[str] = mapped_column(nullable=False)

    __mapper_args__ = {"polymorphic_on": discriminator, "with_polymorphic": "*"}
