from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    Boolean,
    func,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from core.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), nullable=False, unique=True)
    password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )

    tasks = relationship("TaskModel", back_populates="user", lazy="dynamic")

    def hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    def set_password(self, plain_text: str) -> None:
        if len(plain_text.encode("utf-8")) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")
        self.password = self.hash_password(plain_text)


class TokenModel(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, nullable=False, unique=True)
    created_date = Column(DateTime, server_default=func.now())
    user = relationship("UserModel", uselist=False)
