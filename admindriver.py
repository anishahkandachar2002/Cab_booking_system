# admindriver.py

import re
import mysql.connector
from flask import render_template, request, redirect, url_for, session, flash
from db_config import get_connection
from decorators import role_required

# ------------------ Validators ------------------
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^\d{10}$", phone)

def is_valid_vehicle_number(number):
    return re.match(r"^[A-Z]{2}\d{2}[A-Z]{1,2}\d{1,4}$", number, re.IGNORECASE)

# ------------------ Register All Admin Driver Routes ------------------
def register_admin_driver_routes(app):

    @app.route('/manage_drivers')
    @role_required('admin')
    def manage_drivers():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM drivers")
        drivers = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('drivers.html', drivers=drivers)

    @app.route('/add_driver', methods=['POST'])
    @role_required('admin')
    def add_driver():
        phone = request.form['phone']
        vehicle_number = request.form['vehicle_number']
        user_id = request.form['user_id']

        if not is_valid_phone(phone):
            flash("❌ Phone number must be exactly 10 digits.", "danger")
            return redirect(url_for('manage_drivers'))

        if not is_valid_vehicle_number(vehicle_number):
            flash("❌ Invalid vehicle number format. Use format like KA01MB1234 or KA01N9.", "danger")
            return redirect(url_for('manage_drivers'))

        if not is_valid_email(user_id):
            flash("❌ Invalid email format in user ID.", "danger")
            return redirect(url_for('manage_drivers'))

        try:
            data = (
                request.form['name'],
                phone,
                request.form['vehicle_type'],
                user_id,
                request.form['password'],
                vehicle_number,
                request.form['vehicle_company'],
                request.form['vehicle_model']
            )
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO drivers 
                (name, phone, vehicle_type, user_id, password, vehicle_number, vehicle_company, vehicle_model) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, data)
            conn.commit()
            flash("✅ Driver added successfully!", "success")
        except mysql.connector.IntegrityError as e:
            msg = str(e).lower()
            if "phone" in msg:
                flash("❌ A driver with this phone number already exists.", "danger")
            elif "vehicle_number" in msg:
                flash("❌ This vehicle number is already registered.", "danger")
            elif "user_id" in msg:
                flash("❌ This user ID is already taken.", "danger")
            else:
                flash(f"❌ Database error: {str(e)}", "danger")
        except Exception as e:
            flash(f"❌ Unexpected error: {str(e)}", "danger")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
        return redirect(url_for('manage_drivers'))

    @app.route('/delete_driver/<int:id>')
    @role_required('admin')
    def delete_driver(id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM drivers WHERE id = %s", (id,))
            conn.commit()
            flash("✅ Driver deleted successfully.", "success")
        except Exception as e:
            flash(f"❌ Failed to delete driver: {str(e)}", "danger")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
        return redirect(url_for('manage_drivers'))

    @app.route('/approve_driver/<int:id>')
    @role_required('admin')
    def approve_driver(id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE drivers SET approved = NOT approved WHERE id = %s", (id,))
            conn.commit()
            flash("ℹ️ Approval status toggled.", "info")
        except Exception as e:
            flash(f"❌ Approval failed: {str(e)}", "danger")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
        return redirect(url_for('manage_drivers'))

    @app.route('/edit_driver/<int:id>', methods=['POST'])
    @role_required('admin')
    def edit_driver(id):
        phone = request.form['phone']
        vehicle_number = request.form['vehicle_number']
        user_id = request.form['user_id']

        if not is_valid_phone(phone):
            flash("❌ Phone number must be exactly 10 digits.", "danger")
            return redirect(url_for('manage_drivers'))

        if not is_valid_vehicle_number(vehicle_number):
            flash("❌ Invalid vehicle number format. Use format like KA01MB1234 or KA01N9.", "danger")
            return redirect(url_for('manage_drivers'))

        if not is_valid_email(user_id):
            flash("❌ Invalid email format in user ID.", "danger")
            return redirect(url_for('manage_drivers'))

        try:
            data = (
                request.form['name'],
                phone,
                request.form['vehicle_type'],
                user_id,
                request.form['password'],
                vehicle_number,
                request.form['vehicle_company'],
                request.form['vehicle_model'],
                id
            )
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE drivers 
                SET name=%s, phone=%s, vehicle_type=%s, user_id=%s, password=%s,
                    vehicle_number=%s, vehicle_company=%s, vehicle_model=%s
                WHERE id=%s
            """, data)
            conn.commit()
            flash("✅ Driver updated successfully!", "success")
        except mysql.connector.IntegrityError as e:
            msg = str(e).lower()
            if "phone" in msg:
                flash("❌ Another driver already has this phone number.", "danger")
            elif "vehicle_number" in msg:
                flash("❌ This vehicle number is already registered.", "danger")
            elif "user_id" in msg:
                flash("❌ This user ID is already taken.", "danger")
            else:
                flash(f"❌ Update error: {str(e)}", "danger")
        except Exception as e:
            flash(f"❌ Unexpected error: {str(e)}", "danger")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
        return redirect(url_for('manage_drivers'))
