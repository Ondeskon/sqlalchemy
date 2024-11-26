from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from faker import Faker

# Create an engine that connects to the SQLite database
engine = create_engine('sqlite:///database.db')

# Test the connection
connection = engine.connect()
print("Connection to SQLite database successful!")
connection.close()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_of_birth = Column(String)

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Add a test user
new_user = User(name="John Doe", date_of_birth="1990-01-01")
session.add(new_user)
session.commit()

# Verify if the user was added successfully
added_user = session.query(User).filter_by(name="John Doe").first()
if added_user:
    print("User added successfully!")
else:
    print("Failed to add user, rolling back.")
    session.rollback()

print("Table 'users' created and test user added!")

fake = Faker()

# Generate 20 random users
for _ in range(20):
    random_user = User(name=fake.name(), date_of_birth=fake.date_of_birth().strftime('%Y-%m-%d'))
    session.add(random_user)

session.commit()

# Verify if the users were added successfully
added_users = session.query(User).all()
print(f"{len(added_users)} users added successfully!")
# Query users with 'Nixon' in their name

search_string = "Nixon"
nixon_users = session.query(User).filter(User.name.like(f'%{search_string}%')).all()

# Print the users with 'Nixon' in their name
for user in nixon_users:
    print(f"User ID: {user.id}, Name: {user.name}, Date of Birth: {user.date_of_birth}")

    # Delete users with 'Nixon' in their name
    session.delete(user)

session.commit()

# Verify if the users were deleted successfully
deleted_nixon_users = session.query(User).filter(User.name.like(f'%{search_string}%')).all()
if not deleted_nixon_users:
    print(f"All users with '{search_string}' in their name were deleted successfully!")
else:
    print(f"Failed to delete some users with '{search_string}' in their name.")
    # Update all users with the name 'John' to 'Jane Doe'
    
    users_named_john = session.query(User).filter(User.name.like('%John%')).all()
    for user in users_named_john:
        user.name = 'Jane Doe'
    session.commit()

    # Verify if the users were updated successfully
    updated_users = session.query(User).filter(User.name == 'Jane Doe').all()
    if updated_users:
        print(f"All users with 'John' in their name were updated to 'Jane Doe' successfully!")
    else:
        print(f"Failed to update users with 'John' in their name.")