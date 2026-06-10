from sqlalchemy.orm import sessionmaker
from .connection import engine

# can u explain the parameters of sessionmaker?
# - autocommit: This parameter is used to control whether the session should automatically commit transactions. When set to False, you need to explicitly call session.commit() to save changes to the database. In this case, it is set to False, which means that transactions will not be automatically committed.
# - autoflush: This parameter is used to control whether the session should automatically flush changes to the database before executing a query. When set to False, you need to explicitly call session.flush() to send changes to the database. In this case, it is set to False, which means that changes will not be automatically flushed.
# - bind: This parameter is used to specify the database engine or connection that the session should use. In this case, it is set to the engine created in the connection.py file, which means that the session will use that engine to connect to the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)