from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import random

app = Flask(__name__)

DB = Path(__file__).with_name("queueless.db")


# =========================================================
# RESTAURANTS
# =========================================================

RESTAURANTS = [
    ("PizzaBurg Chittagong", "Chattogram", "GEC Circle", "Fast Food"),
    ("Barcode Cafe", "Chattogram", "GEC Circle", "Cafe"),
    ("Handi Restaurant", "Chattogram", "Nasirabad", "Indian"),
    ("Tava Restaurant & Lounge", "Chattogram", "GEC Circle", "Indian"),
    ("Ambrosia Restaurant Ltd", "Chattogram", "Khulshi", "Bangladeshi"),
    ("White Rabbit", "Chattogram", "GEC Circle", "Cafe"),
    ("KRAVE", "Chattogram", "O.R. Nizam Road", "Fast Food"),
    ("Mezetto", "Chattogram", "Khulshi", "Continental"),
    ("Dum Phoonk", "Chattogram", "GEC Circle", "Indian"),
    ("Pitstop Restaurant", "Chattogram", "Khulshi", "Fast Food"),
    ("Royal Hut", "Chattogram", "Agrabad", "Bangladeshi"),
    ("Gharana Restaurant", "Chattogram", "Nasirabad", "Indian"),
    ("SugarBun Restaurant", "Chattogram", "GEC Circle", "Fast Food"),
    ("Meridian Hotel & Restaurant", "Chattogram", "Agrabad", "Bangladeshi"),
    ("Burgerita", "Chattogram", "GEC Circle", "Fast Food"),
    ("Pizza Hut Chattogram", "Chattogram", "GEC Circle", "Pizza"),
    ("Haldi Arabian House", "Chattogram", "Khulshi", "Arabian"),
    ("Lemongrass Restaurant", "Chattogram", "Nasirabad", "Thai"),
    ("Mezzan Haile Ayun", "Chattogram", "Chawkbazar", "Bangladeshi"),
    ("Boomtown Cafe", "Chattogram", "GEC Circle", "Cafe"),
    ("Rio Coffee", "Chattogram", "GEC Circle", "Cafe"),
    ("Grand Mughal Restaurant", "Chattogram", "Agrabad", "Indian"),
    ("Delhi Darbar", "Chattogram", "GEC Circle", "Indian"),
    ("Shawarma House Chittagong", "Chattogram", "GEC Circle", "Arabian"),
    ("Govinda's Hotel & Restaurant", "Chattogram", "Chawkbazar", "Vegetarian"),
    ("The Arrosto", "Chattogram", "Khulshi", "Continental"),
    ("Segafredo Espresso Chittagong", "Chattogram", "GEC Circle", "Cafe"),
    ("Blues & Brown", "Chattogram", "GEC Circle", "Cafe"),
    ("The Green Shadow Restaurant", "Chattogram", "Khulshi", "Bangladeshi"),
    ("Shamiyana", "Chattogram", "Agrabad", "Bangladeshi"),
    ("Kuisine", "Chattogram", "Khulshi", "Asian"),
    ("Secret Recipe Chattogram", "Chattogram", "GEC Circle", "Cafe"),
    ("The Copper Chimney Restaurant", "Chattogram", "Khulshi", "Indian"),
    ("Tokyo Terrace", "Chattogram", "GEC Circle", "Japanese"),
    ("Soho Fine Dining", "Chattogram", "Khulshi", "Continental"),
    ("Omerta", "Chattogram", "GEC Circle", "Cafe"),
    ("Two Spoons", "Chattogram", "GEC Circle", "Cafe"),
    ("Wabi Sabi", "Chattogram", "Khulshi", "Japanese"),
    ("Cook Out Restaurant & Cafe", "Chattogram", "Nasirabad", "Fast Food"),
    ("Foodmarket", "Chattogram", "GEC Circle", "Fast Food"),
    ("Taste Terminal", "Chattogram", "Agrabad", "Fast Food"),
    ("Roadside Kitchen Chittagong", "Chattogram", "GEC Circle", "Fast Food"),
    ("Ozone Lounge", "Chattogram", "Khulshi", "Cafe"),
    ("Zen Table", "Chattogram", "Khulshi", "Asian"),
    ("Ghuddi Rooftop Restaurant", "Chattogram", "GEC Circle", "Bangladeshi"),
    ("Cavien", "Chattogram", "Khulshi", "Continental"),
    ("Cirrus Sky Dining", "Chattogram", "Agrabad", "Fine Dining"),
    ("Lakri Restaurant", "Chattogram", "Chawkbazar", "Bangladeshi"),
    ("Mohora Restaurant", "Chattogram", "Nasirabad", "Bangladeshi"),

    # Other cities
    ("Dhaka Food Hub", "Dhaka", "Dhanmondi", "Bangladeshi"),
    ("Gulshan Grill House", "Dhaka", "Gulshan", "Grill"),
    ("Sylhet Spice Garden", "Sylhet", "Zindabazar", "Bangladeshi"),
    ("Cox Sea View Kitchen", "Cox's Bazar", "Kolatoli", "Seafood"),
    ("Khulna Food Court", "Khulna", "Sonadanga", "Fast Food"),
    ("Rajshahi Taste House", "Rajshahi", "Shaheb Bazar", "Bangladeshi"),
    ("Rangpur Bites", "Rangpur", "Jahaj Company", "Fast Food"),
]


# =========================================================
# SAMPLE MENU
# =========================================================

MENU_TEMPLATES = {

    "Fast Food": [
        ("Classic Beef Burger", 280),
        ("Chicken Burger", 240),
        ("French Fries", 150),
        ("Chicken Wings", 260),
        ("Chicken Cheese Burger", 320),
        ("Soft Drink", 60),
    ],

    "Pizza": [
        ("Chicken Pizza", 350),
        ("Beef Pizza", 390),
        ("Margherita Pizza", 300),
        ("BBQ Chicken Pizza", 420),
        ("Garlic Bread", 160),
        ("Soft Drink", 60),
    ],

    "Cafe": [
        ("Chicken Sandwich", 220),
        ("Pasta Alfredo", 320),
        ("Club Sandwich", 280),
        ("French Fries", 150),
        ("Cold Coffee", 180),
        ("Chocolate Cake", 160),
    ],

    "Indian": [
        ("Chicken Tikka", 320),
        ("Butter Chicken", 360),
        ("Chicken Biryani", 280),
        ("Naan", 70),
        ("Paneer Masala", 300),
        ("Mango Lassi", 140),
    ],

    "Bangladeshi": [
        ("Chicken Biryani", 280),
        ("Beef Tehari", 300),
        ("Chicken Curry", 260),
        ("Plain Rice", 80),
        ("Dal", 90),
        ("Salad", 70),
    ],

    "Arabian": [
        ("Chicken Shawarma", 220),
        ("Beef Shawarma", 260),
        ("Chicken Mandi", 420),
        ("Hummus", 180),
        ("Falafel", 160),
        ("Arabic Salad", 140),
    ],

    "Continental": [
        ("Chicken Steak", 480),
        ("Beef Steak", 580),
        ("Chicken Pasta", 360),
        ("Cream Soup", 180),
        ("Garlic Bread", 160),
        ("Fresh Juice", 140),
    ],

    "Thai": [
        ("Thai Fried Rice", 320),
        ("Chicken Thai Soup", 240),
        ("Pad Thai", 360),
        ("Thai Chicken Curry", 380),
        ("Spring Roll", 180),
        ("Lemon Tea", 100),
    ],

    "Vegetarian": [
        ("Vegetable Biryani", 220),
        ("Paneer Curry", 280),
        ("Dal", 100),
        ("Mixed Vegetable", 180),
        ("Naan", 70),
        ("Fresh Juice", 140),
    ],

    "Asian": [
        ("Chicken Fried Rice", 300),
        ("Chicken Noodles", 280),
        ("Dumplings", 240),
        ("Teriyaki Chicken", 380),
        ("Spring Roll", 180),
        ("Green Tea", 90),
    ],

    "Japanese": [
        ("Chicken Ramen", 420),
        ("Chicken Teriyaki", 450),
        ("Gyoza", 260),
        ("Sushi Set", 520),
        ("Miso Soup", 150),
        ("Green Tea", 90),
    ],

    "Fine Dining": [
        ("Grilled Chicken", 520),
        ("Beef Steak", 680),
        ("Cream Pasta", 420),
        ("Soup of the Day", 220),
        ("Garden Salad", 180),
        ("Fresh Juice", 160),
    ],

    "Grill": [
        ("Chicken Grill", 380),
        ("Beef Steak", 580),
        ("Chicken Wings", 280),
        ("BBQ Platter", 620),
        ("French Fries", 150),
        ("Soft Drink", 60),
    ],

    "Seafood": [
        ("Grilled Fish", 480),
        ("Prawn Curry", 520),
        ("Fish & Chips", 420),
        ("Calamari", 390),
        ("Seafood Fried Rice", 380),
        ("Fresh Juice", 140),
    ],
}


# =========================================================
# DATABASE
# =========================================================

def get_db():

    conn = sqlite3.connect(DB)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db()

    conn.executescript("""
    
    CREATE TABLE IF NOT EXISTS restaurants(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        city TEXT NOT NULL,
        area TEXT NOT NULL,
        cuisine TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS menu_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        available INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER NOT NULL,
        customer_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        items_json TEXT NOT NULL,
        total INTEGER NOT NULL,
        payment_status TEXT NOT NULL DEFAULT 'PENDING',
        payment_method TEXT,
        payment_percent INTEGER NOT NULL DEFAULT 40,
        advance_paid INTEGER NOT NULL DEFAULT 0,
        remaining_amount INTEGER NOT NULL DEFAULT 0,
        order_status TEXT NOT NULL DEFAULT 'PAYMENT_PENDING',
        token TEXT,
        ready_at TEXT,
        created_at TEXT NOT NULL
    );

    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM restaurants"
    ).fetchone()[0]

    if count == 0:

        for restaurant in RESTAURANTS:

            name, city, area, cuisine = restaurant

            cur = conn.execute(
                """
                INSERT INTO restaurants
                (name, city, area, cuisine)
                VALUES (?, ?, ?, ?)
                """,
                (name, city, area, cuisine)
            )

            restaurant_id = cur.lastrowid

            menu = MENU_TEMPLATES.get(
                cuisine,
                MENU_TEMPLATES["Fast Food"]
            )

            for food_name, price in menu:

                conn.execute(
                    """
                    INSERT INTO menu_items
                    (restaurant_id, name, price)
                    VALUES (?, ?, ?)
                    """,
                    (
                        restaurant_id,
                        food_name,
                        price
                    )
                )

    conn.commit()

    conn.close()


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# RESTAURANT SEARCH
# =========================================================

@app.get("/api/restaurants")
def restaurants():

    q = request.args.get(
        "q",
        ""
    ).strip()

    city = request.args.get(
        "city",
        ""
    ).strip()

    conn = get_db()

    sql = """
        SELECT *
        FROM restaurants
        WHERE 1=1
    """

    params = []

    if q:

        sql += """
            AND (
                name LIKE ?
                OR area LIKE ?
                OR cuisine LIKE ?
            )
        """

        search = f"%{q}%"

        params.extend([
            search,
            search,
            search
        ])

    if city and city != "All Bangladesh":

        sql += """
            AND city = ?
        """

        params.append(city)

    sql += """
        ORDER BY city, name
    """

    rows = conn.execute(
        sql,
        params
    ).fetchall()

    conn.close()

    return jsonify([
        {
            "id": row["id"],
            "name": row["name"],
            "city": row["city"],
            "area": row["area"],
            "cuisine": row["cuisine"]
        }
        for row in rows
    ])


# =========================================================
# RESTAURANT MENU
# =========================================================

@app.get("/api/restaurants/<int:restaurant_id>")
def restaurant_details(restaurant_id):

    conn = get_db()

    restaurant = conn.execute(
        """
        SELECT *
        FROM restaurants
        WHERE id = ?
        """,
        (restaurant_id,)
    ).fetchone()

    if not restaurant:

        conn.close()

        return jsonify({
            "error": "Restaurant not found"
        }), 404

    menu = conn.execute(
        """
        SELECT
            id,
            name,
            price,
            available
        FROM menu_items
        WHERE restaurant_id = ?
        ORDER BY id
        """,
        (restaurant_id,)
    ).fetchall()

    conn.close()

    return jsonify({

        "id": restaurant["id"],

        "name": restaurant["name"],

        "city": restaurant["city"],

        "area": restaurant["area"],

        "cuisine": restaurant["cuisine"],

        "menu": [
            dict(item)
            for item in menu
        ]

    })


# =========================================================
# CREATE ORDER
# =========================================================

@app.post("/api/orders")
def create_order():

    import json

    data = request.get_json(
        silent=True
    ) or {}

    restaurant_id = int(
        data.get(
            "restaurant_id",
            0
        )
    )

    customer_name = str(
        data.get(
            "customer_name",
            ""
        )
    ).strip()

    phone = str(
        data.get(
            "phone",
            ""
        )
    ).strip()

    items = data.get(
        "items",
        []
    )

    payment_percent = int(
        data.get(
            "payment_percent",
            40
        )
    )

    # Minimum 40%
    if payment_percent < 40:

        payment_percent = 40

    if payment_percent > 100:

        payment_percent = 100

    if not restaurant_id:

        return jsonify({
            "error": "Restaurant is required."
        }), 400

    if not customer_name:

        return jsonify({
            "error": "Customer name is required."
        }), 400

    if not phone:

        return jsonify({
            "error": "Phone number is required."
        }), 400

    if not items:

        return jsonify({
            "error": "Please select food."
        }), 400

    conn = get_db()

    restaurant = conn.execute(
        """
        SELECT *
        FROM restaurants
        WHERE id = ?
        """,
        (restaurant_id,)
    ).fetchone()

    if not restaurant:

        conn.close()

        return jsonify({
            "error": "Restaurant not found."
        }), 404

    menu_ids = [
        int(item["menu_id"])
        for item in items
    ]

    placeholders = ",".join(
        ["?"] * len(menu_ids)
    )

    menu_rows = conn.execute(
        f"""
        SELECT *
        FROM menu_items
        WHERE restaurant_id = ?
        AND id IN ({placeholders})
        """,
        [restaurant_id] + menu_ids
    ).fetchall()

    menu = {
        row["id"]: row
        for row in menu_rows
    }

    clean_items = []

    total = 0

    for item in items:

        menu_id = int(
            item["menu_id"]
        )

        quantity = max(
            1,
            int(
                item.get(
                    "qty",
                    1
                )
            )
        )

        if menu_id not in menu:

            conn.close()

            return jsonify({
                "error": "Invalid food item."
            }), 400

        food = menu[menu_id]

        if not food["available"]:

            conn.close()

            return jsonify({
                "error": f"{food['name']} is unavailable."
            }), 400

        total += (
            food["price"]
            * quantity
        )

        clean_items.append({

            "menu_id": menu_id,

            "name": food["name"],

            "qty": quantity,

            "unit_price": food["price"]

        })

    advance = round(
        total * payment_percent / 100
    )

    remaining = (
        total - advance
    )

    now = datetime.now()

    cur = conn.execute(
        """
        INSERT INTO orders
        (
            restaurant_id,
            customer_name,
            phone,
            items_json,
            total,
            payment_status,
            payment_method,
            payment_percent,
            advance_paid,
            remaining_amount,
            order_status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            restaurant_id,
            customer_name,
            phone,
            json.dumps(
                clean_items
            ),
            total,
            "PENDING",
            None,
            payment_percent,
            0,
            remaining,
            "PAYMENT_PENDING",
            now.isoformat(
                timespec="seconds"
            )
        )
    )

    order_id = cur.lastrowid

    conn.commit()

    conn.close()

    return jsonify({

        "order_id": order_id,

        "total": total,

        "payment_percent": payment_percent,

        "advance_payment": advance,

        "remaining_payment": remaining,

        "payment_status": "PENDING"

    })


# =========================================================
# PAYMENT
# =========================================================

@app.post("/api/orders/<int:order_id>/pay")
def pay_order(order_id):

    data = request.get_json(
        silent=True
    ) or {}

    method = data.get(
        "method",
        "Card"
    )

    payment_percent = int(
        data.get(
            "payment_percent",
            40
        )
    )

    if payment_percent < 40:

        payment_percent = 40

    if payment_percent > 100:

        payment_percent = 100

    allowed_methods = [
        "bKash",
        "Nagad",
        "Card"
    ]

    if method not in allowed_methods:

        return jsonify({
            "error": "Invalid payment method."
        }), 400

    conn = get_db()

    order = conn.execute(
        """
        SELECT *
        FROM orders
        WHERE id = ?
        """,
        (order_id,)
    ).fetchone()

    if not order:

        conn.close()

        return jsonify({
            "error": "Order not found."
        }), 404

    if order["payment_status"] == "PAID":

        conn.close()

        return jsonify(
            dict(order)
        )

    total = order["total"]

    advance = round(
        total * payment_percent / 100
    )

    remaining = (
        total - advance
    )

    today_orders = conn.execute(
        """
        SELECT COUNT(*)
        FROM orders
        WHERE restaurant_id = ?
        AND date(created_at) = date('now')
        AND payment_status = 'PAID'
        """,
        (
            order["restaurant_id"],
        )
    ).fetchone()[0]

    token = f"Q-{today_orders + 1:03d}"

    ready_at = datetime.now() + timedelta(
        minutes=random.randint(
            20,
            40
        )
    )

    conn.execute(
        """
        UPDATE orders

        SET
            payment_status = 'PAID',

            payment_method = ?,

            payment_percent = ?,

            advance_paid = ?,

            remaining_amount = ?,

            order_status = 'PREPARING',

            token = ?,

            ready_at = ?

        WHERE id = ?
        """,
        (
            method,
            payment_percent,
            advance,
            remaining,
            token,
            ready_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            order_id
        )
    )

    conn.commit()

    updated = conn.execute(
        """
        SELECT *
        FROM orders
        WHERE id = ?
        """,
        (order_id,)
    ).fetchone()

    conn.close()

    return jsonify(
        dict(updated)
    )


# =========================================================
# TRACK ORDER
# =========================================================

@app.get("/api/orders/<int:order_id>")
def track_order(order_id):

    conn = get_db()

    order = conn.execute(
        """
        SELECT
            o.*,
            r.name AS restaurant_name,
            r.city,
            r.area
        FROM orders o

        JOIN restaurants r
        ON r.id = o.restaurant_id

        WHERE o.id = ?
        """,
        (order_id,)
    ).fetchone()

    conn.close()

    if not order:

        return jsonify({
            "error": "Order not found."
        }), 404

    return jsonify(
        dict(order)
    )


# =========================================================
# RESTAURANT ORDER DASHBOARD API
# =========================================================

@app.get("/api/restaurant/<int:restaurant_id>/orders")
def restaurant_orders(restaurant_id):

    conn = get_db()

    orders = conn.execute(
        """
        SELECT
            o.*,
            r.name AS restaurant_name
        FROM orders o

        JOIN restaurants r
        ON r.id = o.restaurant_id

        WHERE o.restaurant_id = ?

        ORDER BY o.id DESC
        """,
        (restaurant_id,)
    ).fetchall()

    conn.close()

    return jsonify([
        dict(order)
        for order in orders
    ])


# =========================================================
# UPDATE ORDER STATUS
# =========================================================

@app.post("/api/orders/<int:order_id>/status")
def update_status(order_id):

    data = request.get_json(
        silent=True
    ) or {}

    status = data.get(
        "status"
    )

    allowed = [
        "PREPARING",
        "READY",
        "COLLECTED",
        "CANCELLED"
    ]

    if status not in allowed:

        return jsonify({
            "error": "Invalid status."
        }), 400

    conn = get_db()

    conn.execute(
        """
        UPDATE orders
        SET order_status = ?
        WHERE id = ?
        """,
        (
            status,
            order_id
        )
    )

    conn.commit()

    order = conn.execute(
        """
        SELECT *
        FROM orders
        WHERE id = ?
        """,
        (order_id,)
    ).fetchone()

    conn.close()

    if not order:

        return jsonify({
            "error": "Order not found."
        }), 404

    return jsonify(
        dict(order)
    )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    init_db()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )