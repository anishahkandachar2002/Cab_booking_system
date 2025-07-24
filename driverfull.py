from flask import render_template, session, redirect, url_for, flash, request
from db_config import get_connection
from decorators import role_required

def register_driver_routes(app):

    # ----------------------------- Home Dashboard -----------------------------
    @app.route('/driver/dashboard')
    @role_required('driver')
    def driver_dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch driver info
        cursor.execute("SELECT * FROM drivers WHERE user_id = %s", (session['user_id'],))
        driver = cursor.fetchone()

        # Fetch ongoing ride
        ongoing_ride = None
        if driver:
            cursor.execute("""
                SELECT id, source AS from_location, destination AS to_location, booking_time, ride_status
                FROM bookings
                WHERE driver_id = %s AND ride_status IN (0, 1)
                ORDER BY booking_time DESC LIMIT 1
            """, (driver['id'],))
            ongoing_ride = cursor.fetchone()

        # Fetch available ride requests
        available_rides = []
        if driver and driver['available'] != 2:
            cursor.execute("""
                SELECT id, source AS from_location, destination AS to_location,
                       booking_time AS ride_datetime, price AS amount
                FROM bookings
                WHERE ride_status = 3 AND driver_id IS NULL
                ORDER BY booking_time DESC
            """)
            available_rides = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('dashboard.html',
                               driver=driver,
                               role='driver',
                               userid=session.get('user_id'),
                               ongoing_ride=ongoing_ride,
                               available_rides=available_rides)

    # ----------------------------- Toggle Availability -----------------------------
    @app.route('/driver/toggle-availability')
    @role_required('driver')
    def toggle_availability():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE drivers
                SET available = NOT available
                WHERE user_id = %s
            """, (session['user_id'],))
            conn.commit()
            flash("Availability status updated.", "success")
        except Exception as e:
            flash(f"Error toggling availability: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('driver_dashboard'))

    # ----------------------------- Logout -----------------------------
    @app.route('/driver/logout')
    def driver_logout():
        if 'user_id' in session:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE drivers SET available = 0 WHERE user_id = %s", (session['user_id'],))
                conn.commit()
            except Exception as e:
                flash(f"⚠️ Error during logout: {str(e)}", "danger")
            finally:
                cursor.close()
                conn.close()
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for('login'))

    # ----------------------------- Edit Profile -----------------------------
    @app.route('/driver/edit-profile', methods=['GET', 'POST'])
    @role_required('driver')
    def edit_profile():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            try:
                form = request.form
                cursor.execute("""
                    UPDATE drivers 
                    SET name=%s, phone=%s, vehicle_type=%s, vehicle_number=%s,
                        vehicle_company=%s, vehicle_model=%s, approved=0, available=0
                    WHERE user_id = %s
                """, (
                    form['name'], form['phone'], form['vehicle_type'],
                    form['vehicle_number'], form['vehicle_company'],
                    form['vehicle_model'], session['user_id']
                ))
                conn.commit()
                session.clear()
                flash("Changes submitted. Awaiting re-approval.", "warning")
                return redirect(url_for('login'))
            except Exception as e:
                flash(f"Error updating profile: {str(e)}", "danger")

        cursor.execute("SELECT * FROM drivers WHERE user_id = %s", (session['user_id'],))
        driver = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_profile.html', driver=driver)

    # ----------------------------- Accept Ride -----------------------------
    @app.route('/driver/accept-ride/<int:booking_id>')
    @role_required('driver')
    def accept_ride(booking_id):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT id FROM drivers WHERE user_id = %s", (session['user_id'],))
            driver = cursor.fetchone()
            if not driver:
                flash("❌ Driver not found.", "danger")
                return redirect(url_for('driver_dashboard'))

            driver_id = driver['id']
            cursor.execute("""
                UPDATE bookings
                SET driver_id = %s, ride_status = 0
                WHERE id = %s AND ride_status = 3
            """, (driver_id, booking_id))
            conn.commit()

            if cursor.rowcount > 0:
                cursor.execute("UPDATE drivers SET available = 2 WHERE id = %s", (driver_id,))
                conn.commit()
                flash("✅ Ride accepted.", "success")
            else:
                flash("❌ Ride was already taken or invalid.", "danger")
        except Exception as e:
            flash(f"Error accepting ride: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('driver_dashboard'))

    # ----------------------------- Start Ride -----------------------------
    @app.route('/driver/start-ride/<int:booking_id>', methods=['POST'])
    @role_required('driver')
    def start_ride(booking_id):
        otp = request.form['otp']
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT otp FROM bookings WHERE id = %s", (booking_id,))
            booking = cursor.fetchone()
            if not booking:
                flash("❌ Booking not found.", "danger")
            elif booking['otp'] != int(otp):
                flash("❌ Incorrect OTP.", "danger")
            else:
                cursor.execute("UPDATE bookings SET ride_status = 1 WHERE id = %s", (booking_id,))
                conn.commit()
                flash("✅ Ride started.", "success")
        except Exception as e:
            flash(f"Error starting ride: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('driver_dashboard'))

    # ----------------------------- Complete Ride -----------------------------
    @app.route('/driver/complete-ride/<int:booking_id>')
    @role_required('driver')
    def complete_ride(booking_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE bookings
                SET ride_status = 2
                WHERE id = %s AND driver_id = (
                    SELECT id FROM drivers WHERE user_id = %s
                ) AND ride_status = 1
            """, (booking_id, session['user_id']))
            conn.commit()

            cursor.execute("UPDATE drivers SET available = 1 WHERE user_id = %s", (session['user_id'],))
            conn.commit()

            flash("✅ Ride completed.", "success")
        except Exception as e:
            flash(f"Error completing ride: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('driver_dashboard'))

    # ----------------------------- View Requests -----------------------------
    @app.route('/driver/view-requests')
    @role_required('driver')
    def driver_view_requests():
        return redirect(url_for('driver_dashboard'))

    # ----------------------------- View Driver Bookings -----------------------------
    @app.route('/driver/bookings')
    @role_required('driver')
    def driver_view_bookings():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM drivers WHERE user_id = %s", (session['user_id'],))
        driver = cursor.fetchone()
        if not driver:
            cursor.close()
            conn.close()
            return redirect(url_for('driver_dashboard'))

        driver_id = driver['id']
        cursor.execute("""
            SELECT 
                b.id,
                b.source AS from_location,
                b.destination AS to_location,
                b.booking_time,
                b.ride_status,
                u.name AS customer_name
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            WHERE b.driver_id = %s
            ORDER BY b.booking_time DESC
        """, (driver_id,))
        bookings = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('view_bookings.html', bookings=bookings)
