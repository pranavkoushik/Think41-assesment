from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os

# Import database models and session
from database import SessionLocal, engine, Base, User, Order

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Customer Order Dashboard API",
    description="API for accessing customer and order data",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Customer Order Dashboard API",
        "status": "running",
        "version": "1.0.0"
    }

# Get all customers with pagination
@app.get("/api/customers/")
async def get_customers(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    customers = db.query(User).offset(skip).limit(limit).all()
    return {
        "status": "success",
        "count": len(customers),
        "data": [
            {
                "id": customer.id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "orders_count": len(customer.orders) if hasattr(customer, 'orders') else 0
            }
            for customer in customers
        ]
    }

# Get customer by ID with order details
@app.get("/api/customers/{customer_id}")
async def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(User).filter(User.id == customer_id).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {
        "status": "success",
        "data": {
            "id": customer.id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone_number": customer.phone_number,
            "created_at": customer.created_at.isoformat() if customer.created_at else None,
            "orders_count": len(customer.orders) if hasattr(customer, 'orders') else 0,
            "orders": [
                {
                    "order_id": order.id,
                    "status": order.status,
                    "created_at": order.created_at.isoformat() if order.created_at else None,
                    "updated_at": order.updated_at.isoformat() if order.updated_at else None
                }
                for order in customer.orders
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
