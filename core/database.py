from sqlalchemy import create_engine, Column, Integer, String, ForeignKey 
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///E:/Educationals/FastAPI-tutorial-service/sqlite.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String())


def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()