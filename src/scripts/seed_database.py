#!/usr/bin/env python3
"""
Database seeding script for development environment
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app.models.database import SessionLocal, DriveThruSession, Order, OrderItem
from src.app.config import settings

def seed_database():
    """Seed database with sample data"""
    db = SessionLocal()

    try:
        # Create sample session
        session = DriveThruSession(
            vehicle_info="Blue Toyota Camry",
            lane_number=1,
            status="active"
        )
        db.add(session)
        db.flush()  # Get the ID

        # Create sample order
        order = Order(
            session_id=session.id,
            order_number="DT20240001",
            status="ordering",
            total_amount=15.97
        )
        db.add(order)
        db.flush()

        # Create sample order items
        items = [
            OrderItem(
                order_id=order.id,
                menu_item_id=1,
                quantity=1,
                unit_price=8.99,
                item_total=8.99,
                selected_modifiers={"size": "large"}
            ),
            OrderItem(
                order_id=order.id,
                menu_item_id=2,
                quantity=1,
                unit_price=3.49,
                item_total=3.49,
                selected_modifiers={"size": "medium"}
            ),
            OrderItem(
                order_id=order.id,
                menu_item_id=3,
                quantity=1,
                unit_price=1.99,
                item_total=1.99
            )
        ]

        for item in items:
            db.add(item)

        db.commit()
        print("✅ Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()