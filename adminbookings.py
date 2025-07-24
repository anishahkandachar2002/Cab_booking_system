# adminbookings.py

from flask import render_template, session, redirect, url_for, flash
from db_config import get_connection
from decorators import role_required

def register_admin_booking_routes(app):
    
    # ------------------ View All Bookings ------------------
    @app.route('/view_bookings')
    @role_required('admin')
    def view_bookings():
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT b.id, u.name AS user_name, d.name AS driver_name,
                       b.source, b.destination, b.booking_time
                FROM bookings b
                JOIN users u ON b.user_id = u.id
                JOIN drivers d ON b.driver_id = d.id
                ORDER BY b.booking_time DESC
            """)
            bookings = cursor.fetchall()
        except Exception as e:
            flash(f"❌ Failed to load bookings: {str(e)}", "danger")
            bookings = []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
        return render_template('bookings.html', bookings=bookings)
