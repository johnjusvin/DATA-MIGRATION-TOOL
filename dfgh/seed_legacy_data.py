import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables from the .env file in the parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_connection_string():
    # Fetch credentials from .env
    host = os.getenv('LEGACY_DB_HOST', 'localhost')
    port = os.getenv('LEGACY_DB_PORT', '5432')
    db = os.getenv('LEGACY_DB_NAME', 'postgres')
    user = os.getenv('LEGACY_DB_USER', 'postgres')
    password = os.getenv('LEGACY_DB_PASSWORD', 'your_password')
    
    # Using PostgreSQL as you requested
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"

def seed_data():
    print(f"Connecting to Legacy Database...")
    engine = create_engine(get_connection_string())
    
    with engine.begin() as conn:
        # 1. Create LEGACY CUST_MASTER table
        # Notice the old data types: VARCHAR(8) for dates, VARCHAR(1) for booleans
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS CUST_MASTER (
                CUST_ID INTEGER PRIMARY KEY,
                CUST_NAME VARCHAR(100),
                BIRTH_DT VARCHAR(8),
                STATUS VARCHAR(1)
            )
        """))
        print("Created legacy table: CUST_MASTER")

        # 2. Create LEGACY ORD_MASTER table
        # Notice the old data types: VARCHAR for amounts and dates
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ORD_MASTER (
                ORD_ID INTEGER PRIMARY KEY,
                CUST_NO INTEGER,
                ORD_DT VARCHAR(8),
                TOTAL_AMT VARCHAR(20)
            )
        """))
        print("Created legacy table: ORD_MASTER")

        # Clear existing data so we don't get primary key collisions on multiple runs
        conn.execute(text("TRUNCATE TABLE ORD_MASTER;"))
        conn.execute(text("TRUNCATE TABLE CUST_MASTER;"))

        # 3. Generate Mock Data for CUST_MASTER in batches
        print("Generating 100,000 rows of mock data for CUST_MASTER...")
        cust_batch = []
        for i in range(1, 100001):
            name = f"JOHN DOE {i}" # legacy ALL CAPS
            # Legacy Date format YYYYMMDD as string
            birth_dt = (datetime(1970, 1, 1) + timedelta(days=random.randint(0, 10000))).strftime('%Y%m%d')
            status = random.choice(['A', 'I']) # A for Active, I for Inactive
            
            cust_batch.append({
                "cust_id": i,
                "cust_name": name,
                "birth_dt": birth_dt,
                "status": status
            })

            # Insert in batches of 10,000 to be fast
            if i % 10000 == 0:
                conn.execute(text(
                    "INSERT INTO CUST_MASTER (CUST_ID, CUST_NAME, BIRTH_DT, STATUS) VALUES (:cust_id, :cust_name, :birth_dt, :status)"
                ), cust_batch)
                cust_batch = []
                print(f"Inserted {i} / 100000 customers...")
        
        # 4. Generate Mock Data for ORD_MASTER in batches
        print("Generating 300,000 rows of mock data for ORD_MASTER...")
        ord_batch = []
        for i in range(1, 300001):
            cust_no = random.randint(1, 100000)
            ord_dt = (datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1000))).strftime('%Y%m%d')
            total_amt = f"{random.uniform(10.0, 500.0):.2f}" # Stored as string
            
            ord_batch.append({
                "ord_id": i,
                "cust_no": cust_no,
                "ord_dt": ord_dt,
                "total_amt": total_amt
            })

            # Insert in batches of 10,000
            if i % 10000 == 0:
                conn.execute(text(
                    "INSERT INTO ORD_MASTER (ORD_ID, CUST_NO, ORD_DT, TOTAL_AMT) VALUES (:ord_id, :cust_no, :ord_dt, :total_amt)"
                ), ord_batch)
                ord_batch = []
                print(f"Inserted {i} / 300000 orders...")
        
if __name__ == '__main__':
    seed_data()
    print("\n✅ Legacy data generation complete! Your old database is now populated.")
