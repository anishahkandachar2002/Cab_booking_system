# userfull.py
from flask import render_template, request, redirect, url_for, session, flash
from db_config import get_connection
import random

def register_user_routes(app):

    def login_required(func):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session or session.get('role') != 'user':
                flash("Unauthorized access. Please login.", "danger")
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper

    @app.route('/user/dashboard')
    @login_required
    def user_dashboard():
        user_id = session['user_id']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                b.*,
                d.name AS driver_name,
                d.phone AS driver_phone,
                CONCAT(d.vehicle_company, ' ', d.vehicle_model, ' (', d.vehicle_number, ')') AS driver_vehicle
            FROM bookings b
            LEFT JOIN drivers d ON b.driver_id = d.id
            WHERE b.user_id = %s AND b.ride_status IN (0, 1, 3)
            ORDER BY b.booking_time DESC LIMIT 1
        """, (user_id,))
        ride = cursor.fetchone()

        cursor.close()
        conn.close()

        return render_template('dashboard.html', user_name=session.get('user_id'), ride=ride)

    @app.route('/user/edit-profile', methods=['GET', 'POST'])
    @login_required
    def edit_user_profile():
        user_id = session['user_id']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            try:
                name = request.form['name']
                phone = request.form['phone']
                email = request.form['email']

                cursor.execute("UPDATE users SET name=%s, phone=%s, email=%s WHERE id=%s",
                               (name, phone, email, user_id))
                conn.commit()
                flash("✅ Profile updated successfully!", "success")
                return redirect(url_for('dashboard'))
            except Exception as e:
                flash(f"❌ Error updating profile: {str(e)}", "danger")

        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_profileuser.html', user=user)

    @app.route('/user/book-ride', methods=['GET', 'POST'])
    @login_required
    def book_ride():
        user_id = session['user_id']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        otp = str(random.randint(1000, 9999))

        cursor.execute("SELECT DISTINCT from_location AS location FROM prices UNION SELECT DISTINCT to_location FROM prices")
        locations = [row['location'] for row in cursor.fetchall()]

        car_options = []
        selected_from = selected_to = selected_car_type = ""

        if request.method == 'POST':
            from_loc = request.form.get('from_location')
            to_loc = request.form.get('to_location')
            selected_from = from_loc
            selected_to = to_loc

            if from_loc == to_loc:
                flash("❗ Source and destination cannot be the same.", "warning")
            elif 'show_options' in request.form:
                cursor.execute("""
                    SELECT car_type, price FROM prices
                    WHERE (from_location = %s AND to_location = %s)
                       OR (from_location = %s AND to_location = %s)
                """, (from_loc, to_loc, to_loc, from_loc))
                car_options = cursor.fetchall()
                if not car_options:
                    flash("❌ No pricing available for this route.", "danger")

            elif 'confirm_booking' in request.form:
                selected_car_type = request.form.get('car_type')
                cursor.execute("""
                    SELECT price FROM prices
                    WHERE ((from_location = %s AND to_location = %s)
                       OR  (from_location = %s AND to_location = %s))
                      AND car_type = %s
                """, (from_loc, to_loc, to_loc, from_loc, selected_car_type))
                result = cursor.fetchone()
                if result:
                    price = result['price']
                    cursor.execute("""
                        INSERT INTO bookings (user_id, source, destination, car_type, price, booking_time, ride_status, otp)
                        VALUES (%s, %s, %s, %s, %s, NOW(), 3, %s)
                    """, (user_id, from_loc, to_loc, selected_car_type, price, otp))
                    conn.commit()
                    flash("✅ Ride booked successfully!", "success")
                    return redirect(url_for('ride_history'))
                else:
                    flash("❌ Invalid price route/car combo.", "danger")

        cursor.close()
        conn.close()

        return render_template('book_ride.html',
                               from_locations=locations,
                               to_locations=locations,
                               car_options=car_options,
                               selected_from=selected_from,
                               selected_to=selected_to,
                               selected_car_type=selected_car_type)

    @app.route('/user/ride-history')
    @login_required
    def ride_history():
        user_id = session['user_id']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

    # Get all past rides
        cursor.execute("""
        SELECT 
            b.*, 
            d.name AS driver_name,
            d.phone AS driver_phone,
            CONCAT(d.vehicle_company, ' ', d.vehicle_model, ' (', d.vehicle_number, ')') AS driver_vehicle
        FROM bookings b
        LEFT JOIN drivers d ON b.driver_id = d.id
        WHERE b.user_id = %s
        ORDER BY b.booking_time DESC
    """, (user_id,))
        rides = cursor.fetchall()

    # Get the latest ride (status 0, 1, or 3)
        cursor.execute("""
        SELECT 
            b.*,
            d.name AS driver_name,
            d.phone AS driver_phone,
            CONCAT(d.vehicle_company, ' ', d.vehicle_model, ' (', d.vehicle_number, ')') AS driver_vehicle
        FROM bookings b
        LEFT JOIN drivers d ON b.driver_id = d.id
        WHERE b.user_id = %s AND b.ride_status IN (0, 1, 3)
        ORDER BY b.booking_time DESC LIMIT 1
    """, (user_id,))
        ride = cursor.fetchone()

        cursor.close()
        conn.close()
        return render_template('ride_history.html', rides=rides, ride=ride)

