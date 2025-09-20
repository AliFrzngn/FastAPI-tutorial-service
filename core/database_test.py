from sqlalchemy import create_engine, Column, Integer, String, Boolean, or_ ,and_, not_, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from models import User, Order, engine

SQLALCHEMY_DATABASE_URL = "sqlite:///E:/Educationals/FastAPI-tutorial-service/sqlite.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30))
    last_name = Column(String(30), nullable=True)
    age = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)


    def __repr__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name})"


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    city = Column(String())
    state = Column(String())
    zip_code = Column(String())

Base.metadata.create_all(engine)

session = SessionLocal()

#ali = User(first_name="ali", age=27)
#session.add(ali)
#session.commit()


#maryam = User(first_name="maryam", age=32)
#hashem = User(first_name="hashem", age=46)
#users = [maryam, hashem]
#session.add_all(users)
#session.commit()

#users = session.query(User).all()
#print(users)


#user.last_name = "farzanegan"
#session.commit()


user = session.query(User).filter_by(first_name="ali").first()

if user:
    session.delete(user)
    session.commit()


users_all = session.query(User).all()

users_filtered = session.query(User).filter(User.age >=25).all()

print("ALL User: ", len(users_all))
print ("Filtered users: ", len(users_filtered))

users_filterd = session.query(User).filter(User.age >= 25, User.first_name == "ali").all()

# add multiple filters
# query all users with age greater than or equal to 25 and name equals to something
users_filtered = session.query(User).filter(User.age >=25,User.first_name == "ali").all()

# or you can use where
users_filtered = session.query(User).where(User.age >=25,User.first_name == "ali").all()

# users with similar name contianing specific substrings
users_similar_name = session.query(User).filter(User.first_name.like("%ali%")).all()

# users with case insensitive match
users_similar_name = session.query(User).filter(User.first_name.ilike("%ali%")).all()

# users with starting and ending chars
users_starting_ali = session.query(User).filter(User.first_name.like("Ali%")).all()
users_ending_ali = session.query(User).filter(User.first_name.like("%Ali")).all()



# query those who has ali as name or age above 25
users_filtered = session.query(User).filter(or_(User.age >=25,User.name == "ali")).all()

# query those who has ali as name and age above 25
users_filtered = session.query(User).filter(and_(User.age >=25,User.name == "ali")).all()

# query those whos name is not ali
users_filtered = session.query(User).filter(not_(User.name == "ali")).all()

# getting users which are note named ali or age between 35,60
users = session.query(User).filter(or_(not_(User.name == "ali"),and_(User.age >35,User.age<60)))

# 1. Count Total Users
total_users = session.query(func.count(User.id)).scalar()
print("Total Users:", total_users)

# 2. Find the Average Age of Users
average_age = session.query(func.avg(User.age)).scalar()
print("Average Age:", average_age)

# 3. Find the Maximum and Minimum Age
max_age = session.query(func.max(User.age)).scalar()
min_age = session.query(func.min(User.age)).scalar()
print(f"Max Age: {max_age}, Min Age: {min_age}")

# 4. Find the Total Number of Orders
total_orders = session.query(func.count(Order.id)).scalar()
print("Total Orders:", total_orders)

# 5. Find the Sum of All Order Amounts
total_revenue = session.query(func.sum(Order.total_amount)).scalar()
print("Total Revenue:", total_revenue)

# 6. Find the Average Order Value
average_order_value = session.query(func.avg(Order.total_amount)).scalar()
print("Average Order Value:", average_order_value)

# 7. Find Users Who Have Placed the Most Orders
most_active_users = session.query(
    User.name, func.count(Order.id).label("order_count")
).join(Order).group_by(User.id).order_by(func.count(Order.id).desc()).limit(5).all()
print("Top 5 Active Users by Order Count:", most_active_users)

# 8. Find Users with the Highest Total Spending
top_spenders = session.query(
    User.name, func.sum(Order.total_amount).label("total_spent")
).join(Order).group_by(User.id).order_by(func.sum(Order.total_amount).desc()).limit(5).all()
print("Top 5 Users by Spending:", top_spenders)

# 9. Find Users Who Have Not Placed Any Orders
users_without_orders = session.query(User).outerjoin(Order).filter(Order.id == None).all()
print("Users Without Orders:", [user.name for user in users_without_orders])

# 10. Find the Most Recent Order Date
latest_order_date = session.query(func.max(Order.created_at)).scalar()
print("Most Recent Order Date:", latest_order_date)

# Close the session
session.close()

# Example 1: Count Users with a Specific Condition (Raw SQL)
query = text("SELECT COUNT(*) FROM user WHERE age >= :min_age")
result = session.execute(query, {"min_age": 25}).scalar()
print("Users with age >= 25:", result)

# Example 2: Find the Average Age of Users (Raw SQL)
query = text("SELECT AVG(age) FROM user")
result = session.execute(query).scalar()
print("Average Age of Users:", result)

# Example 3: Get Users with a Specific Name (Raw SQL)
query = text("SELECT * FROM user WHERE name = :name")
result = session.execute(query, {"name": "Ali"}).fetchall()
print("Users named Ali:", [user.name for user in result])

# Example 4: Aggregate Query for the Total Revenue (Raw SQL)
query = text("SELECT SUM(total_amount) FROM order")
result = session.execute(query).scalar()
print("Total Revenue:", result)

# Close the session
session.close()

# 1. محاسبه تعداد سفارشات برای هر کاربر
users_order_count = session.query(
    User.id, User.name, func.count(Order.id).label("order_count")
).join(Order).group_by(User.id).all()

for user in users_order_count:
    print(f"User: {user.name}, Order Count: {user.order_count}")

# 2. محاسبه مجموع مبلغ سفارشات برای هر کاربر
users_total_spent = session.query(
    User.id, User.name, func.sum(Order.total_amount).label("total_spent")
).join(Order).group_by(User.id).all()

for user in users_total_spent:
    print(f"User: {user.name}, Total Spent: {user.total_spent}")