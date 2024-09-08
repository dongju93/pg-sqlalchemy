import base64
from datetime import date, datetime
from typing import Optional

from sqlalchemy import (
    TIMESTAMP,
    VARCHAR,
    Boolean,
    Date,
    ForeignKey,
    Integer,
    LargeBinary,
    Numeric,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ActorTable(Base):
    __tablename__ = "actor"

    actor_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(45), nullable=False)
    last_name: Mapped[str] = mapped_column(VARCHAR(45), nullable=False)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


class AddressTable(Base):
    __tablename__ = "address"

    address_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    address: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    address2: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    district: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.city_id"), nullable=False
    )
    postal_code: Mapped[Optional[str]] = mapped_column(
        VARCHAR(10), nullable=True
    )
    phone: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


class CategoryTable(Base):
    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(VARCHAR(25), nullable=False)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


class CityTable(Base):
    __tablename__ = "city"

    city_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    country_id: Mapped[int] = mapped_column(
        ForeignKey("country.country_id"), nullable=False
    )
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


class CountryTable(Base):
    __tablename__ = "country"

    country_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    country: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


class CustomerTable(Base):
    __tablename__ = "customer"

    customer_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    store_id: Mapped[int] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(VARCHAR(45), nullable=False)
    last_name: Mapped[str] = mapped_column(VARCHAR(45), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    address_id: Mapped[int] = mapped_column(
        ForeignKey("address.address_id"), nullable=False
    )
    activebool: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    create_date: Mapped[date] = mapped_column(Date, nullable=False)
    last_update: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP, nullable=True
    )
    active: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class FilmTable(Base):
    __tablename__ = "film"

    film_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    release_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    language_id: Mapped[int] = mapped_column(
        ForeignKey("language.language_id"), nullable=False
    )
    rental_duration: Mapped[int] = mapped_column(
        Integer, nullable=False, default=3
    )
    rental_rate: Mapped[float] = mapped_column(
        Numeric(4, 2), nullable=False, default=4.99
    )
    length: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    replacement_cost: Mapped[float] = mapped_column(
        Numeric(5, 2), nullable=False, default=19.99
    )
    rating: Mapped[Optional[str]] = mapped_column(VARCHAR, nullable=True)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    special_features: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(Text), nullable=True
    )
    fulltext: Mapped[str] = mapped_column(TSVECTOR, nullable=False)


class FilmActorTable(Base):
    __tablename__ = "film_actor"

    actor_id: Mapped[int] = mapped_column(
        ForeignKey("actor.actor_id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True,
    )
    film_id: Mapped[int] = mapped_column(
        ForeignKey("film.film_id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True,
    )
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


class FilmCategoryTable(Base):
    __tablename__ = "film_category"

    film_id: Mapped[int] = mapped_column(
        ForeignKey("film.film_id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            "category.category_id", ondelete="RESTRICT", onupdate="CASCADE"
        ),
        primary_key=True,
    )
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


class InventoryTable(Base):
    __tablename__ = "inventory"

    inventory_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    film_id: Mapped[int] = mapped_column(
        ForeignKey("film.film_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    store_id: Mapped[int] = mapped_column(nullable=False)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


class LanguageTable(Base):
    __tablename__ = "language"

    language_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


class PaymentTable(Base):
    __tablename__ = "payment"

    payment_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey(
            "customer.customer_id", ondelete="RESTRICT", onupdate="CASCADE"
        ),
        nullable=False,
    )
    staff_id: Mapped[int] = mapped_column(
        ForeignKey("staff.staff_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    rental_id: Mapped[int] = mapped_column(
        ForeignKey(
            "rental.rental_id", ondelete="SET NULL", onupdate="CASCADE"
        ),
        nullable=False,
    )
    amount: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    payment_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


class RentalTable(Base):
    __tablename__ = "rental"

    rental_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    rental_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    inventory_id: Mapped[int] = mapped_column(
        ForeignKey(
            "inventory.inventory_id", ondelete="RESTRICT", onupdate="CASCADE"
        ),
        nullable=False,
    )
    customer_id: Mapped[int] = mapped_column(
        ForeignKey(
            "customer.customer_id", ondelete="RESTRICT", onupdate="CASCADE"
        ),
        nullable=False,
    )
    return_date: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP, nullable=True
    )
    staff_id: Mapped[int] = mapped_column(
        ForeignKey("staff.staff_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


class StaffTable(Base):
    __tablename__ = "staff"

    staff_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(45), nullable=False)
    last_name: Mapped[str] = mapped_column(VARCHAR(45), nullable=False)
    address_id: Mapped[int] = mapped_column(
        ForeignKey(
            "address.address_id", ondelete="RESTRICT", onupdate="CASCADE"
        ),
        nullable=False,
    )
    email: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    store_id: Mapped[int] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    username: Mapped[str] = mapped_column(VARCHAR(16), nullable=False)
    password: Mapped[Optional[str]] = mapped_column(VARCHAR(40), nullable=True)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    picture: Mapped[Optional[bytes]] = mapped_column(
        LargeBinary, nullable=True
    )

    # picture 필드를 Base64로 인코딩된 문자열로 반환
    @hybrid_property
    def picture_base64(self) -> Optional[str]:
        if self.picture:
            picture_str = base64.b64encode(self.picture).decode("utf-8")
            return picture_str
        return None


class StoreTable(Base):
    __tablename__ = "store"

    store_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    manager_staff_id: Mapped[int] = mapped_column(
        ForeignKey("staff.staff_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    address_id: Mapped[int] = mapped_column(
        ForeignKey(
            "address.address_id", ondelete="RESTRICT", onupdate="CASCADE"
        ),
        nullable=False,
    )
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
