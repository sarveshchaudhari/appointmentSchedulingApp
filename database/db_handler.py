import sqlite3
from typing import List, Dict, Any

DB_FILE = "appointments.db"

# ... (get_db_connection, init_db, add_appointment functions are unchanged) ...

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn


def init_db():
    """Initializes the database and creates the appointments table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        customer_phone TEXT NOT NULL,
        appointment_datetime TEXT NOT NULL UNIQUE,
        service_type TEXT NOT NULL,
        duration_minutes INTEGER NOT NULL DEFAULT 60,
        status TEXT NOT NULL CHECK (status IN ('CONFIRMED', 'CANCELLED')) DEFAULT 'CONFIRMED',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()


def add_appointment(name: str, phone: str, dt: str, service: str) -> Dict[str, Any]:
    """Adds a new appointment to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO appointments (customer_name, customer_phone, appointment_datetime, service_type) VALUES (?, ?, ?, ?)",
            (name, phone, dt, service)
        )
        conn.commit()
        appointment_id = cursor.lastrowid
        return {"status": "success", "id": appointment_id}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "This time slot is already booked."}
    finally:
        conn.close()


def search_appointments(criteria: str, value: str) -> List[Dict[str, Any]]:
    """Searches for appointments by customer_name, service_type, or date."""
    conn = get_db_connection()
    cursor = conn.cursor()

    allowed_criteria = {
        "customer_name": "customer_name",
        "service_type": "service_type",
        "date": "date(appointment_datetime)"
    }

    if criteria not in allowed_criteria:
        return []

    query = f"SELECT * FROM appointments WHERE {allowed_criteria[criteria]} = ? AND status = 'CONFIRMED'"
    cursor.execute(query, (value,))

    appointments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return appointments

# --- NEW FUNCTION ---
def get_all_appointments() -> List[Dict[str, Any]]:
    """Retrieves all confirmed appointments from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Order by date to make the list more useful
    query = "SELECT * FROM appointments WHERE status = 'CONFIRMED' ORDER BY appointment_datetime"
    cursor.execute(query)
    appointments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return appointments
# --------------------


def delete_appointments(criteria: str, value: str) -> int:
    # ... (function is unchanged) ...
    conn = get_db_connection()
    cursor = conn.cursor()

    allowed_criteria = {
        "customer_name": "customer_name",
        "service_type": "service_type",
        "date": "date(appointment_datetime)",
        "id": "id"
    }
    if criteria not in allowed_criteria:
        return 0

    query = f"DELETE FROM appointments WHERE {allowed_criteria[criteria]} = ?"
    cursor.execute(query, (value,))
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted_count

def update_appointment(identifier_value: str, field_to_update: str, new_value: str) -> int:
    # ... (function is unchanged) ...
    conn = get_db_connection()
    cursor = conn.cursor()

    allowed_fields = ["customer_phone", "appointment_datetime", "service_type"]
    if field_to_update not in allowed_fields:
        return 0

    query = f"UPDATE appointments SET {field_to_update} = ? WHERE customer_name = ?"

    cursor.execute(query, (new_value, identifier_value))
    updated_count = cursor.rowcount
    conn.commit()
    conn.close()
    return updated_count