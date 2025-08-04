import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session, Session
from datetime import datetime
from typing import Generator
import os

# Database URL configuration
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Scoped session for thread safety
SessionScoped = scoped_session(SessionLocal)

# Database setup
Base = declarative_base()
Base.query = SessionScoped.query_property()

# Dependency to get DB session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    price = Column(Float, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="product")

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

def init_db():
    """Initialize the database and create tables."""
    # Create SQLite database in the project root
    db_path = os.path.join(os.path.dirname(__file__), '..', 'ecommerce.db')
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create all tables
    Base.metadata.create_all(engine)
    print(f"Database initialized at {os.path.abspath(db_path)}")
    return engine

def load_csv_to_table(engine, csv_path, table_name, chunksize=10000):
    """Load data from a CSV file into a database table in chunks."""
    print(f"Loading data from {os.path.basename(csv_path)} to {table_name}...")
    
    # Get the total number of rows for progress tracking
    total_rows = sum(1 for _ in open(csv_path, 'r', encoding='utf-8')) - 1  # Subtract header
    print(f"Total rows to process: {total_rows:,}")
    
    # Read and insert data in chunks
    processed_rows = 0
    for chunk in pd.read_csv(csv_path, chunksize=chunksize, low_memory=False):
        # Clean column names (remove special characters, convert to lowercase)
        chunk.columns = [col.strip().lower().replace(' ', '_').replace('-', '_') for col in chunk.columns]
        
        # Convert date columns if they exist
        date_columns = [col for col in chunk.columns if 'date' in col or 'created' in col or 'updated' in col]
        for col in date_columns:
            if col in chunk.columns:
                try:
                    chunk[col] = pd.to_datetime(chunk[col], errors='coerce')
                except Exception as e:
                    print(f"Warning: Could not convert column '{col}' to datetime: {e}")
        
        # Insert the chunk into the database
        chunk.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',
            index=False,
            method='multi',
            chunksize=1000
        )
        
        processed_rows += len(chunk)
        print(f"Processed {processed_rows:,}/{total_rows:,} rows ({processed_rows/total_rows*100:.1f}%)")
    
    print(f"Successfully loaded data into {table_name}")

def load_data(engine, data_dir):
    """Load data from all CSV files in the data directory."""
    # Map of CSV files to their target tables and any required transformations
    csv_mapping = {
        'users.csv': 'users',
        'products.csv': 'products',
        'orders.csv': 'orders',
        'order_items.csv': 'order_items'
    }
    
    # Process each CSV file
    for csv_file, table_name in csv_mapping.items():
        csv_path = os.path.join(data_dir, csv_file)
        if os.path.exists(csv_path):
            load_csv_to_table(engine, csv_path, table_name)
        else:
            print(f"Warning: {csv_file} not found in {data_dir}")
    
    print("Data loading complete!")

if __name__ == "__main__":
    import argparse
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Initialize database and load data')
    parser.add_argument('--data-dir', default=os.path.join('..', 'archive'),
                      help='Directory containing the CSV files (default: ../archive)')
    args = parser.parse_args()
    
    print("Initializing database...")
    engine = init_db()
    
    # Check if data directory exists and has CSV files
    data_dir = os.path.abspath(args.data_dir)
    if not os.path.exists(data_dir):
        print(f"\nError: Data directory not found: {data_dir}")
        print("Please specify the correct directory containing the CSV files using --data-dir")
        exit(1)
    
    # Check for CSV files
    required_files = ['users.csv', 'orders.csv', 'products.csv', 'order_items.csv']
    missing_files = [f for f in required_files if not os.path.exists(os.path.join(data_dir, f))]
    
    if missing_files:
        print("\nError: The following required files are missing:")
        for file in missing_files:
            print(f"- {file}")
        print(f"\nPlease ensure all files are present in: {data_dir}")
        exit(1)
    
    # Load data into the database
    print("\nStarting data import...")
    load_data(engine, data_dir)
    
    print("\nDatabase setup complete!")
