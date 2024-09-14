from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    # Relationships to link categories and budgets to the user
    transactions = relationship("Transaction", back_populates="user")
    categories = relationship("Category", back_populates="user")
    budgets = relationship("Budget", back_populates="user")


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)

    user = relationship("User", back_populates="transactions")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ForeignKey to link to User

    # Relationship to link category to a user
    user = relationship("User", back_populates="categories")



class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)  # ForeignKey to link to Category
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ForeignKey to link to User
    amount = Column(Float, nullable=False)
    period = Column(String, nullable=False)

    # Relationships to link budget to category and user
    category = relationship("Category")  # Link budget to a category
    user = relationship("User", back_populates="budgets")
