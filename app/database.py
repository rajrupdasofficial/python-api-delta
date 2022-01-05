from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL='postgresql://postgres:passkey@localhost/fastapi'
engine=create_engine(SQL_ALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()


#initializing database file
def get_db():
	db=SessionLocal()
	try:
		yield db
	finally:
		db.close()