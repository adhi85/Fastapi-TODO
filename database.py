from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://vkdcsgco:ujbL47ZtNSBKUJtZhpRjmQBfZyHUMpEA@floppy.db.elephantsql.com/vkdcsgco"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:meenus@localhost/TodoApplicationDatabase"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()