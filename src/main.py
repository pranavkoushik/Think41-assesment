from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import os
from datetime import datetime

# Import database models and session
from database import SessionLocal, engine, Base, User, Order, OrderItem, Product

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
                    "id": order.id,
                    "status": order.status,
                    "created_at": order.created_at.isoformat() if order.created_at else None,
                    "updated_at": order.updated_at.isoformat() if order.updated_at else None,
                    "items_count": len(order.items) if hasattr(order, 'items') else 0
                }
                for order in customer.orders
            ]
        }
    }

# Get all orders for a specific customer
@app.get("/api/customers/{customer_id}/orders", response_model=Dict[str, Any])
async def get_customer_orders(
    customer_id: int,
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    # Check if customer exists
    customer = db.query(User).filter(User.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found"
        )
    
    # Build query
    query = db.query(Order).filter(Order.user_id == customer_id)
    
    # Apply filters if provided
    if status:
        query = query.filter(Order.status == status)
    if start_date:
        query = query.filter(Order.created_at >= start_date)
    if end_date:
        # Add one day to include the end date
        query = query.filter(Order.created_at < (end_date + timedelta(days=1)))
    
    # Get total count for pagination
    total = query.count()
    
    # Apply pagination
    orders = query.offset(skip).limit(limit).all()
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "total_orders": total,
        "count": len(orders),
        "data": [
            {
                "id": order.id,
                "status": order.status,
                "created_at": order.created_at.isoformat() if order.created_at else None,
                "updated_at": order.updated_at.isoformat() if order.updated_at else None,
                "items_count": len(order.items) if hasattr(order, 'items') else 0,
                "total_amount": sum(item.price * item.quantity for item in order.items) if hasattr(order, 'items') else 0
            }
            for order in orders
        ]
    }

# Get specific order details
@app.get("/api/orders/{order_id}", response_model=Dict[str, Any])
async def get_order_details(
    order_id: int,
    db: Session = Depends(get_db)
):
    # Get order with related data
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    # Get customer details
    customer = db.query(User).filter(User.id == order.user_id).first()
    
    # Calculate order total
    order_total = sum(item.price * item.quantity for item in order.items) if hasattr(order, 'items') else 0
    
    return {
        "status": "success",
        "data": {
            "order": {
                "id": order.id,
                "status": order.status,
                "created_at": order.created_at.isoformat() if order.created_at else None,
                "updated_at": order.updated_at.isoformat() if order.updated_at else None,
                "total_amount": order_total,
                "items_count": len(order.items) if hasattr(order, 'items') else 0
            },
            "customer": {
                "id": customer.id if customer else None,
                "name": f"{customer.first_name} {customer.last_name}" if customer else "Unknown",
                "email": customer.email if customer else None
            },
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.product.name if hasattr(item, 'product') and item.product else "Unknown Product",
                    "quantity": item.quantity,
                    "unit_price": item.price,
                    "total_price": item.price * item.quantity
                }
                for item in order.items
            ] if hasattr(order, 'items') else []
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
