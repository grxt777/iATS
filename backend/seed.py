"""
Database Seed Script
Creates realistic test data for demo and development
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from app.core.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.driver import Driver
from app.models.vehicle import Vehicle, VehicleType, VehicleStatus
from app.models.order import Order, CargoType, OrderStatus


def seed():
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            print("🌱 Seeding initial data...")

            # 1. Create Users
            shipper = User(
                email="shipper@elogs.uz",
                hashed_password="fakehashpassword",
                full_name="OOO E-Trade Shipper",
                phone="+998901234567",
                company_name="E-Trade Tashkent",
                inn="123456789",
                role=UserRole.SHIPPER,
                is_verified=True
            )
            carrier = User(
                email="carrier@elogs.uz",
                hashed_password="fakehashpassword",
                full_name="TransService Carrier",
                phone="+998907654321",
                company_name="TransService LLC",
                inn="987654321",
                role=UserRole.CARRIER,
                is_verified=True
            )
            driver_user = User(
                email="driver@elogs.uz",
                hashed_password="fakehashpassword",
                full_name="Alisher Qodirov",
                phone="+998931112233",
                role=UserRole.DRIVER,
                is_verified=True
            )
            admin_user = User(
                email="admin@elogs.uz",
                hashed_password="fakehashpassword",
                full_name="System Admin",
                phone="+998901000000",
                role=UserRole.ADMIN,
                is_verified=True
            )
            db.add_all([shipper, carrier, driver_user, admin_user])
            db.commit()

            # 2. Create Driver
            driver = Driver(
                user_id=driver_user.id,
                full_name=driver_user.full_name,
                pinfl="30101901234567",
                phone=driver_user.phone,
                license_number="AA123456",
                license_category="BC",
                experience_years=5,
                is_available=True,
                is_verified=True,
                average_rating=4.9,
                total_trips=247,
                safe_trips=240
            )
            db.add(driver)
            db.commit()

            # 3. Create Vehicles
            vehicles = [
                Vehicle(
                    owner_id=carrier.id,
                    driver_id=driver.id,
                    type=VehicleType.TRUCK_LARGE,
                    brand="MAN",
                    model="TGX",
                    license_plate="01 777 AAA",
                    capacity_kg=22000.0,
                    volume_m3=80.0,
                    current_lat=41.2995,
                    current_lng=69.2401,
                    current_address="Tashkent Depot",
                    status=VehicleStatus.AVAILABLE,
                    cost_per_km_uzs=12000,
                    average_rating=4.9,
                    success_rate=0.97,
                    total_trips=247,
                    successful_trips=240,
                    has_international_permit=True,
                    permit_countries="RU,KZ,CN,TR",
                ),
                Vehicle(
                    owner_id=carrier.id,
                    type=VehicleType.REFRIGERATOR,
                    brand="Volvo",
                    model="FH16",
                    license_plate="01 456 BCD",
                    capacity_kg=20000.0,
                    volume_m3=70.0,
                    current_lat=41.3111,
                    current_lng=69.2797,
                    current_address="Tashkent → Samarkand",
                    status=VehicleStatus.IN_TRANSIT,
                    cost_per_km_uzs=15000,
                    average_rating=4.7,
                    success_rate=0.94,
                    total_trips=189,
                    successful_trips=178,
                    has_international_permit=True,
                ),
                Vehicle(
                    owner_id=carrier.id,
                    type=VehicleType.FLATBED,
                    brand="Scania",
                    model="R500",
                    license_plate="01 123 EFG",
                    capacity_kg=25000.0,
                    volume_m3=120.0,
                    current_lat=40.3833,
                    current_lng=71.7833,
                    current_address="Fergana Hub",
                    status=VehicleStatus.AVAILABLE,
                    cost_per_km_uzs=14000,
                    average_rating=4.8,
                    success_rate=0.95,
                    total_trips=156,
                    successful_trips=148,
                ),
                Vehicle(
                    owner_id=carrier.id,
                    type=VehicleType.VAN,
                    brand="Ford",
                    model="Transit",
                    license_plate="01 333 KLM",
                    capacity_kg=3000.0,
                    volume_m3=15.0,
                    current_lat=41.2995,
                    current_lng=69.2401,
                    current_address="Tashkent City",
                    status=VehicleStatus.AVAILABLE,
                    cost_per_km_uzs=8000,
                    average_rating=4.5,
                    success_rate=0.92,
                    total_trips=312,
                    successful_trips=287,
                ),
            ]
            db.add_all(vehicles)
            db.commit()

            # 4. Create Orders
            orders = [
                Order(
                    id=1247,
                    user_id=shipper.id,
                    cargo_type=CargoType.PERISHABLE,
                    cargo_name="Fresh Apples",
                    cargo_description="Refrigerated apples transport to Samarkand",
                    weight_kg=20000.0,
                    volume_m3=70.0,
                    pickup_address="Tashkent Depot",
                    pickup_lat=41.2995,
                    pickup_lng=69.2401,
                    delivery_address="Samarkand Hub",
                    delivery_lat=39.6542,
                    delivery_lng=66.9597,
                    pickup_date=datetime.now(),
                    delivery_deadline=datetime.now() + timedelta(hours=8),
                    urgency_score=8,
                    budget_uzs=1500000.0,
                    status=OrderStatus.PENDING,
                ),
                Order(
                    id=1246,
                    user_id=shipper.id,
                    cargo_type=CargoType.GENERAL,
                    cargo_name="Textile Fabric",
                    cargo_description="Rolls of cotton fabric",
                    weight_kg=15000.0,
                    volume_m3=60.0,
                    pickup_address="Bukhara Warehouse",
                    pickup_lat=39.7747,
                    pickup_lng=64.4286,
                    delivery_address="Navoi Industrial Zone",
                    delivery_lat=40.1063,
                    delivery_lng=65.3776,
                    pickup_date=datetime.now() + timedelta(days=1),
                    urgency_score=5,
                    budget_uzs=800000.0,
                    status=OrderStatus.PENDING,
                ),
                Order(
                    id=1245,
                    user_id=shipper.id,
                    cargo_type=CargoType.GENERAL,
                    cargo_name="Construction Metal",
                    cargo_description="Steel beams and plates",
                    weight_kg=25000.0,
                    volume_m3=90.0,
                    pickup_address="Fergana Factory",
                    pickup_lat=40.3833,
                    pickup_lng=71.7833,
                    delivery_address="Tashkent Construction Site",
                    delivery_lat=41.2995,
                    delivery_lng=69.2401,
                    pickup_date=datetime.now() - timedelta(days=1),
                    urgency_score=3,
                    budget_uzs=2100000.0,
                    status=OrderStatus.IN_TRANSIT,
                ),
                Order(
                    id=1244,
                    user_id=shipper.id,
                    cargo_type=CargoType.GENERAL,
                    cargo_name="Electronics",
                    cargo_description="Consumer electronics - laptops and phones",
                    weight_kg=5000.0,
                    volume_m3=20.0,
                    pickup_address="Tashkent Electronics Hub",
                    pickup_lat=41.2995,
                    pickup_lng=69.2401,
                    delivery_address="Bukhara Retail Center",
                    delivery_lat=39.7747,
                    delivery_lng=64.4286,
                    pickup_date=datetime.now() - timedelta(days=2),
                    urgency_score=6,
                    budget_uzs=1200000.0,
                    status=OrderStatus.DELIVERED,
                ),
                Order(
                    id=1243,
                    user_id=shipper.id,
                    cargo_type=CargoType.DANGEROUS,
                    cargo_name="Chemical Drums",
                    cargo_description="Industrial chemicals - ADR Class 3",
                    weight_kg=12000.0,
                    volume_m3=40.0,
                    adr_class=3,
                    adr_subclass="3",
                    pickup_address="Chirchiq Chemical Plant",
                    pickup_lat=41.4689,
                    pickup_lng=69.5861,
                    delivery_address="Samarkand Industrial",
                    delivery_lat=39.6542,
                    delivery_lng=66.9597,
                    pickup_date=datetime.now() + timedelta(days=2),
                    urgency_score=9,
                    budget_uzs=3000000.0,
                    status=OrderStatus.PENDING,
                ),
            ]
            db.add_all(orders)
            db.commit()

            print("✅ Database seeded successfully!")
            print(f"   - 4 users created")
            print(f"   - 1 driver created")
            print(f"   - 4 vehicles created")
            print(f"   - 5 orders created")
            print(f"\n You can now start the backend:")
            print(f"   uvicorn app.main:app --reload")
        else:
            print("ℹ️  Database already has records, skipping seed.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
