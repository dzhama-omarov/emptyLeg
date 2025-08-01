from sqlalchemy import (
    Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Text
)
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum

Base = declarative_base()


class UserTypeEnum(Enum):
    charterer = "Charterer"
    carrier = "Carrier"


class CargoTypeEnum(Enum):
    general = "General Cargo"
    special = "Special Cargo"
    dangerous = "Dangerous Goods"
    temperature_sensitive = "Temperature Sensitive Cargo"
    perishable = "Perishable Goods"
    live_animals = "Live Animals"


class CurrencyEnum(Enum):
    usd = "USD"
    eur = "EUR"
    rub = "RUB"
    gbp = "GBP"
    cny = "CNY"


class ContractStatusEnum(Enum):
    pending = "Pending"
    signed = "Signed"
    cancelled = "Cancelled"


class PaymentStatusEnum(Enum):
    paid = "Paid"
    pending = "Pending"
    overdue = "Overdue"
    cancelled = "Cancelled"
    refunded = "Refunded"
    partially_paid = "Partially Paid"
    partially_refunded = "Partially Refunded"
    partially_paid_overdue = "Partially Paid & Overdue"
    partially_refunded_overdue = "Partially Refunded & Overdue"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    fullName = Column(String, index=True)
    company = Column(String, index=True)
    userType = Column(Enum(UserTypeEnum))
    userRep = Column(Float)
    password = Column(String)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('users.id'), nullable=False)
    orderNumber = Column(Integer, unique=True, nullable=False)
    orderDate = Column(DateTime, nullable=False)
    partnerUser = Column(Integer, ForeignKey('users.id'), nullable=False)
    aircraftType = Column(String, nullable=False)
    flightNumber = Column(String, nullable=False)
    departureDate = Column(DateTime, nullable=False)
    departureCity = Column(String, nullable=False)
    departureAirport = Column(String, nullable=False)
    departureCargoType = Column(Enum(CargoTypeEnum), nullable=False)
    departureCargoWeight = Column(Float, nullable=False)
    departureCargoVolume = Column(Float, nullable=False)
    arrivalDate = Column(DateTime, nullable=False)
    arrivalCity = Column(String, nullable=False)
    arrivalAirport = Column(String, nullable=False)
    arrivalCargoType = Column(Enum(CargoTypeEnum), nullable=False)
    arrivalCargoWeight = Column(Float, nullable=False)
    arrivalCargoVolume = Column(Float, nullable=False)
    roundTrip = Column(Boolean, nullable=False)
    orderPrice = Column(Float, nullable=False)
    orderCurrency = Column(Enum(CurrencyEnum), nullable=False)
    paymentStatus = Column(Enum(PaymentStatusEnum), nullable=False)
    contractOrder = Column(ForeignKey("contracts.id"))
    orderStatus = Column(String, nullable=False)
    isEmptyLegMatch = Column(Boolean, nullable=False)

    user = relationship('User', back_populates='orders')


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    charterer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    carrier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contract_date = Column(DateTime, nullable=False)
    effective_from = Column(DateTime, nullable=False)
    effective_to = Column(DateTime, nullable=True)
    contract_status = Column(Enum(ContractStatusEnum), nullable=False)
    contract_file_url = Column(String, nullable=True)
    terms_summary = Column(Text, nullable=True)
    created_at = Column(DateTime)

    order = relationship("Order", back_populates="contract", uselist=False)
    charterer = relationship(
        "Users",
        foreign_keys=[charterer_id],
        back_populates="charter_contracts"
    )
    carrier = relationship(
        "Users",
        foreign_keys=[carrier_id],
        back_populates="carrier_contracts"
    )
