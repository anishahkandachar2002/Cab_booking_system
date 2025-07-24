from flask import Flask, render_template, request, redirect, session, flash, url_for
from db_config import get_connection
from decorators import role_required
from adminuser import register_admin_routes
from admindriver import register_admin_driver_routes
from adminbookings import register_admin_booking_routes
from adminpricing import register_admin_pricing_routes
from driverfull import register_driver_routes
from userfull import register_user_routes
from auth_users import AdminUser, DriverUser, RegularUser


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Register route modules
register_admin_routes(app)
register_admin_driver_routes(app)
register_admin_booking_routes(app)
register_admin_pricing_routes(app)
register_driver_routes(app)
register_user_routes(app)

# ----------------------------
# Login Route
# ----------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid'].strip()
        password = request.form['password'].strip()
        role = request.form['role'].strip().lower()

        role_classes = {
            'admin': AdminUser,
            'driver': DriverUser,
            'user': RegularUser
        }

        if role not in role_classes:
            flash("Invalid role selected.", "danger")
            return redirect('/')

        user_class = role_classes[role]
        user_obj = user_class(userid, password)
        user_data = user_obj.authenticate()

        if user_data:
            session['role'] = role

            if role == 'admin':
                session['user_id'] = user_data['username']
            elif role == 'user':
                session['user_id'] = user_data['id']
                session['user_name'] = user_data['name']
            elif role == 'driver':
                session['user_id'] = user_data['user_id']
                session['driver_name'] = user_data['name']

            flash("Login successful!", "success")
            return redirect('/dashboard')
        else:
            if role == 'driver':
                flash("⛔ Driver not approved or invalid credentials.", "warning")
            else:
                flash("❌ Invalid credentials.", "danger")
            return redirect('/')

    return render_template('login.html')




# ----------------------------
# Role-Based Dashboard
# ----------------------------
@app.route('/dashboard')
def dashboard():
    print("=== SESSION DEBUG ===")
    print("session.get('user_id') =", session.get('user_id'))
    print("session.get('role') =", session.get('role'))

    if not session.get('user_id') or not session.get('role'):
        flash("Unauthorized access. Please login.", "danger")
        return redirect('/')

    return render_template('dashboard.html', role=session['role'], userid=session['user_id'])












@app.route('/register-user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        user_id = request.form['user_id']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, phone, email, password, user_id) VALUES (%s, %s, %s, %s, %s)",
                       (name, phone, email, password, user_id))
        conn.commit()
        cursor.close()
        conn.close()

        flash("✅ User registered! You can now log in.", "success")
        return redirect('/')

    return render_template('register_user.html')


@app.route('/register-driver', methods=['GET', 'POST'])
def register_driver():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        vehicle_type = request.form['vehicle_type']
        user_id = request.form['user_id']
        password = request.form['password']
        vehicle_number = request.form['vehicle_number']
        vehicle_company = request.form['vehicle_company']
        vehicle_model = request.form['vehicle_model']

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO drivers 
                (name, phone, vehicle_type, user_id, password, vehicle_number, vehicle_company, vehicle_model, approved)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, phone, vehicle_type, user_id, password,
                  vehicle_number, vehicle_company, vehicle_model, 0))

            conn.commit()
            flash("✅ Driver registered successfully. Awaiting admin approval.", "success")

        except Exception as e:
            print("❌ Registration Error:", e)
            flash("❌ Registration failed: " + str(e), "danger")

        finally:
            cursor.close()
            conn.close()

        return redirect('/')

    return render_template('register_driver.html')


















# ----------------------------
# Logout
# ----------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect('/')

# ----------------------------
# Run App
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
