# adminuser.py

import re
import mysql.connector
from flask import render_template, request, redirect, url_for, flash, session
from db_config import get_connection
from decorators import role_required

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^\d{10}$", phone)

def register_admin_routes(app):

    @app.route('/manage_users')
    @role_required('admin')
    def manage_users():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('users.html', users=users)

    @app.route('/add_user', methods=['POST'])
    @role_required('admin')
    def add_user():
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        user_id = request.form['user_id']

        if not is_valid_email(email):
            flash("❌ Invalid email format.", "danger")
            return redirect(url_for('manage_users'))

        if not is_valid_phone(phone):
            flash("❌ Phone number must be exactly 10 digits.", "danger")
            return redirect(url_for('manage_users'))

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (name, phone, email, password, user_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, phone, email, password, user_id))
            conn.commit()
            flash("✅ User added successfully!", "success")
        except mysql.connector.IntegrityError as e:
            msg = str(e).lower()
            if "email" in msg:
                flash("❌ Email already exists.", "danger")
            elif "phone" in msg:
                flash("❌ Phone number already exists.", "danger")
            elif "user_id" in msg:
                flash("❌ User ID already exists.", "danger")
            else:
                flash(f"❌ Failed to add user: {str(e)}", "danger")
        except Exception as e:
            flash(f"❌ Unexpected error: {str(e)}", "danger")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

        return redirect(url_for('manage_users'))

    @app.route('/edit_user/<int:id>', methods=['POST'])
    @role_required('admin')
    def edit_user(id):
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        user_id = request.form['user_id']

        if not is_valid_email(email):
            flash("❌ Invalid email format.", "danger")
            return redirect(url_for('manage_users'))

        if not is_valid_phone(phone):
            flash("❌ Phone number must be exactly 10 digits.", "danger")
            return redirect(url_for('manage_users'))

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users
                SET name=%s, phone=%s, email=%s, password=%s, user_id=%s
                WHERE id=%s
            """, (name, phone, email, password, user_id, id))
            conn.commit()
            flash("✅ User updated successfully!", "success")
        except mysql.connector.IntegrityError as e:
            msg = str(e).lower()
            if "email" in msg:
                flash("❌ Email already exists.", "danger")
            elif "phone" in msg:
                flash("❌ Phone number already exists.", "danger")
            elif "user_id" in msg:
                flash("❌ User ID already exists.", "danger")
            else:
                flash(f"❌ Failed to update user: {str(e)}", "danger")
        except Exception as e:
            flash(f"❌ Unexpected error: {str(e)}", "danger")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

        return redirect(url_for('manage_users'))

    @app.route('/delete_user/<int:id>')
    @role_required('admin')
    def delete_user(id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (id,))
            conn.commit()
            flash("✅ User deleted successfully!", "success")
        except Exception as e:
            flash(f"❌ Failed to delete user: {str(e)}", "danger")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

        return redirect(url_for('manage_users'))
