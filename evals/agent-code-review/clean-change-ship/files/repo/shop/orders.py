def add_order(conn, customer, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    cur = conn.execute(
        "INSERT INTO orders (customer, amount) VALUES (?, ?)", (customer, amount)
    )
    conn.commit()
    return cur.lastrowid
