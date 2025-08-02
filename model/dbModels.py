from sqlalchemy import (
    Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Text
)
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()


class UserTypeEnum(enum.Enum):
    charterer = "Charterer"
    carrier = "Carrier"
    broker = "Broker"


class CargoTypeEnum(enum.Enum):
    general = "General Cargo"
    special = "Special Cargo"
    dangerous = "Dangerous Goods"
    temperature_sensitive = "Temperature Sensitive Cargo"
    perishable = "Perishable Goods"
    live_animals = "Live Animals"


class CurrencyEnum(enum.Enum):
    usd = "USD"
    eur = "EUR"
    rub = "RUB"
    gbp = "GBP"
    cny = "CNY"


class ContractStatusEnum(enum.Enum):
    pending = "Pending"
    signed = "Signed"
    cancelled = "Cancelled"


class PaymentStatusEnum(enum.Enum):
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
    userType = Column(SQLEnum(UserTypeEnum))
    userRep = Column(Float)
    password = Column(String)

    orders = relationship("Order", back_populates="user", foreign_keys="Order.userId")
    joined_orders = relationship("Order", back_populates="partner", foreign_keys="Order.partnerUser")
    chartererContracts = relationship("Contract", back_populates="charterer", foreign_keys="Contract.chartererId")
    carrierContracts = relationship("Contract", back_populates="carrier", foreign_keys="Contract.carrierId")


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
    departureCargoType = Column(SQLEnum(CargoTypeEnum), nullable=False)
    departureCargoWeight = Column(Float, nullable=False)
    departureCargoVolume = Column(Float, nullable=False)
    arrivalDate = Column(DateTime, nullable=False)
    arrivalCity = Column(String, nullable=False)
    arrivalAirport = Column(String, nullable=False)
    arrivalCargoType = Column(SQLEnum(CargoTypeEnum), nullable=False)
    arrivalCargoWeight = Column(Float, nullable=False)
    arrivalCargoVolume = Column(Float, nullable=False)
    roundTrip = Column(Boolean, nullable=False)
    orderPrice = Column(Float, nullable=False)
    orderCurrency = Column(SQLEnum(CurrencyEnum), nullable=False)
    paymentStatus = Column(SQLEnum(PaymentStatusEnum), nullable=False)
    contractOrder = Column(ForeignKey("contracts.id"))
    orderStatus = Column(String, nullable=False)
    isEmptyLegMatch = Column(Boolean, nullable=False)

    user = relationship("User", back_populates="orders", foreign_keys=[userId])
    partner = relationship("User", back_populates="joined_orders", foreign_keys=[partnerUser])
    contract = relationship("Contract", back_populates="orders")


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    chartererId = Column(Integer, ForeignKey("users.id"), nullable=False)
    carrierId = Column(Integer, ForeignKey("users.id"), nullable=False)
    contractDate = Column(DateTime, nullable=False)
    effectiveFrom = Column(DateTime, nullable=False)
    effectiveTo = Column(DateTime, nullable=True)
    contractStatus = Column(SQLEnum(ContractStatusEnum), nullable=False)
    contractFileUrl = Column(String, nullable=True)
    termsSummary = Column(Text, nullable=True)
    createdAt = Column(DateTime)

    orders = relationship("Order", back_populates="contract")
    charterer = relationship("User", back_populates="chartererContracts", foreign_keys=[chartererId])
    carrier = relationship("User", back_populates="carrierContracts", foreign_keys=[carrierId])
