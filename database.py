import sqlite3

def init_db():
    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_name TEXT,
            status TEXT,
            amount REAL
        )
    ''')
    
    # Insert sample records
    sample_orders = [
        ('ORD-101', 'Alice', 'Shipped', 35.00),
        ('ORD-102', 'Bob', 'Delivered', 120.00),
        ('ORD-103', 'Charlie', 'Processing', 15.00)
    ]
    
    cursor.executemany("INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?)", sample_orders)
    conn.commit()
    conn.close()
    print("Database initialized successfully with sample data.")

if __name__ == "__main__":
    init_db()