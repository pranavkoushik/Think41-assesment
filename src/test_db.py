import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Database setup
Base = declarative_base()

class TestTable(Base):
    __tablename__ = 'test_table'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

def test_db_connection():
    try:
        # Try to create a simple SQLite database
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test.db'))
        engine = create_engine(f'sqlite:///{db_path}')
        
        # Create tables
        Base.metadata.create_all(engine)
        
        # Verify table was created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\nDatabase created at: {db_path}")
        print(f"Tables in database: {tables}")
        
        return True
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing database connection and table creation...")
    success = test_db_connection()
    if success:
        print("\n✅ Database test successful!")
    else:
        print("\n❌ Database test failed. Please check the error message above.")
