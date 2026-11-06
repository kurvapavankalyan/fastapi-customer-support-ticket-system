from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    role = Column(String, default="Client", nullable=False)

    tickets = relationship(
        "Ticket",
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class Ticket(Base):
    __tablename__ = "ticket"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("customers.ID"), nullable=False)
    message = Column(String, nullable=False)
    category = Column(String, default="To be Update")
    priority = Column(String, default="None")
    sentiment = Column(String, default="None")
    status = Column(String, default="Pending")
    reply = Column(String, default="Pending")

    customer = relationship("Customer", back_populates="tickets")
