from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "mysql://root:@localhost:3306/codeburst"
SQLALCHEMY_DATABASE_URL = "postgresql://root:1@localhost:5432/kardinahku" #+"?gssencmode=disable"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
