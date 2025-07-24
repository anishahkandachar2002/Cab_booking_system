import mysql.connector
from flask import render_template, request, redirect, url_for, flash
from db_config import get_connection
from decorators import role_required

def register_admin_pricing_routes(app):

    # ------------------ View All Prices ------------------
    @app.route('/manage_pricing')
    @role_required('admin')
    def manage_pricing():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM prices")
        prices = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('pricing.html', prices=prices)

    # ------------------ Add Price ------------------
    @app.route('/add_price', methods=['POST'])
    @role_required('admin')
    def add_price():
        from_loc = request.form['from_location'].strip()
        to_loc = request.form['to_location'].strip()
        car_type = request.form['car_type']
        price = request.form['price'].strip()

        # Validations
        if not from_loc or not to_loc or not price:
            flash("❌ All fields are required.", "danger")
            return redirect(url_for('manage_pricing'))

        if from_loc.lower() == to_loc.lower():
            flash("❌ From and To locations cannot be the same.", "danger")
            return redirect(url_for('manage_pricing'))

        if not price.replace('.', '', 1).isdigit() or float(price) <= 0:
            flash("❌ Price must be a positive number.", "danger")
            return redirect(url_for('manage_pricing'))

        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Check for duplicates
            cursor.execute("""
                SELECT * FROM prices
                WHERE LEAST(from_location, to_location) = LEAST(%s, %s)
                  AND GREATEST(from_location, to_location) = GREATEST(%s, %s)
                  AND car_type = %s
            """, (from_loc, to_loc, from_loc, to_loc, car_type))

            if cursor.fetchone():
                flash("⚠️ This route with the selected car type already exists.", "warning")
            else:
                cursor.execute("""
                    INSERT INTO prices (from_location, to_location, car_type, price)
                    VALUES (%s, %s, %s, %s)
                """, (from_loc, to_loc, car_type, price))
                conn.commit()
                flash("✅ Route pricing added!", "success")
        except mysql.connector.Error as e:
            flash(f"❌ DB error while adding: {str(e)}", "danger")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
        return redirect(url_for('manage_pricing'))

    # ------------------ Edit Price ------------------
    @app.route('/edit_price/<int:id>', methods=['POST'])
    @role_required('admin')
    def edit_price(id):
        from_loc = request.form['from_location'].strip()
        to_loc = request.form['to_location'].strip()
        car_type = request.form['car_type']
        price = request.form['price'].strip()

        if not from_loc or not to_loc or not price:
            flash("❌ All fields are required.", "danger")
            return redirect(url_for('manage_pricing'))

        if from_loc.lower() == to_loc.lower():
            flash("❌ Source and destination cannot be the same.", "danger")
            return redirect(url_for('manage_pricing'))

        if not price.replace('.', '', 1).isdigit() or float(price) <= 0:
            flash("❌ Price must be a positive number.", "danger")
            return redirect(url_for('manage_pricing'))

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Prevent duplicate (excluding current id)
            cursor.execute("""
                SELECT * FROM prices
                WHERE id != %s
                  AND LEAST(from_location, to_location) = LEAST(%s, %s)
                  AND GREATEST(from_location, to_location) = GREATEST(%s, %s)
                  AND car_type = %s
            """, (id, from_loc, to_loc, from_loc, to_loc, car_type))

            if cursor.fetchone():
                flash("⚠️ Updating to this route would cause a duplicate entry.", "warning")
            else:
                cursor.execute("""
                    UPDATE prices
                    SET from_location=%s, to_location=%s, car_type=%s, price=%s
                    WHERE id=%s
                """, (from_loc, to_loc, car_type, price, id))
                conn.commit()
                flash("✅ Route updated successfully!", "success")
        except mysql.connector.Error as e:
            flash(f"❌ DB error during update: {str(e)}", "danger")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
        return redirect(url_for('manage_pricing'))

    # ------------------ Delete Price ------------------
    @app.route('/delete_price/<int:id>')
    @role_required('admin')
    def delete_price(id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM prices WHERE id = %s", (id,))
            conn.commit()
            flash("✅ Route deleted!", "success")
        except mysql.connector.Error as e:
            flash(f"❌ Deletion failed: {str(e)}", "danger")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
        return redirect(url_for('manage_pricing'))
