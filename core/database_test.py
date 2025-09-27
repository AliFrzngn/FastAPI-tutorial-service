from sqlalchemy import create_engine, Column, Integer, String, Boolean, Table, ForeignKey, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
from sqlalchemy.orm import backref
SQLALCHEMY_DATABASE_URL = "sqlite:///E:/Educationals/FastAPI-tutorial-service/sqlite.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


enorollments = Table("enrollments", Base.metadata, 
                     Column("id", Integer, primary_key=True, autoincrement=True),
                     Column("user_id", Integer, ForeignKey("users.id")),
                     Column("course_id", Integer, ForeignKey("courses.id")),
                     Column("enrolled_date", DateTime(), default=datetime.now),
                     UniqueConstraint("user_id", "course_id", name="unique_user_course_enrolled")
                     )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30))
    email = Column(String(30), nullable=True)
    password = Column(String(10))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    addresses = relationship("Address",backref="user")
    profile = relationship("Profile", backref="user", uselist=False)
    posts = relationship("Post", backref="user")
    courses = relationship("Course", secondary=enorollments, back_populates="attendees")
    def __repr__(self):
        return f"User(id={self.id}, courses={self.courses})"

    

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    city = Column(String())
    state = Column(String())
    zip_code = Column(String())
    #user = relationship("User",back_populates="addresses")


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name= Column(String())
    last_name= Column(String())
    bio = Column(String(), nullable=True)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String())
    content = Column(Text())
    comments =relationship("Comment", backref="post")
    created_date = Column(DateTime(), default=datetime.now)
    update_date = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    def __repr__(self):
        return f"Post(id={self.id}, title={self.title})"

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    content = Column(Text())
    #parent = relationship("Comment", back_populates="children", remote_side=[id])
    children = relationship("Comment", backref=backref("parent", remote_side=[id]))


    def __repr__(self):
        return f"Comment(id={self.id}, post_id={self.post_id}, user_id={self.user_id}, parent_id={self.parent_id}, content={self.content})"
    
class Course(Base):
    __tablename__= "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String())
    descrpition = Column(Text())

    created_date = Column(DateTime(), default=datetime.now)

    attendees = relationship("User", secondary=enorollments, back_populates="courses")
    
    def __repr__(self):
        return f"Course(id={self.id}, title={self.title})"

Base.metadata.create_all(engine)

session = SessionLocal()
