#!/usr/bin/env python3
"""0. User model"""
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    """Class inititialization"""
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    email = Column("email", String(250), nullable=False)
    hashed_password = Column("hashed_password", String(250), nullable=False)
    session_id = Column("session_id", String(250), nullable=True)
    reset_token = Column("reset_token", String(250), nullable=True)
