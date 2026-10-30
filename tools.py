import sqlite3

def get_order_status(order_id: str) -> str:
    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()
    cursor.execute("SELECT status, amount FROM orders WHERE order_id = ?", (order_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return f"Order {order_id} is currently '{row[0]}' with an order total of ${row[1]:.2f}."
    return f"Order ID '{order_id}' was not found in our system."

def process_refund(order_id: str, amount: float) -> str:
    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = 'Refunded' WHERE order_id = ?", (order_id,))
    conn.commit()
    conn.close()
    return f"Refund of ${amount:.2f} successfully processed for Order {order_id}."