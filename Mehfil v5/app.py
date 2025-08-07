from flask import Flask, request, jsonify, render_template
import pymysql, os

app = Flask(__name__)

# Get the directory where app.py is located
app_dir = os.path.dirname(os.path.abspath(__file__))

# Set the templates folder to the same directory as app.py
app = Flask(__name__, template_folder=app_dir)

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'DEMONking912',
    'database': 'mehfil_booking'
}

# Route to Handle Booking Form Submission
@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    city = data.get('city')
    date = data.get('date')
    time_slot = data.get('time_slot')
    payment_method = data.get('payment')

    connection = None  # Initialize connection to ensure it's accessible in finally block

    try:
        # Connect to Database
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # Check for Existing Booking
        query = "SELECT * FROM bookings WHERE city = %s AND date = %s AND time_slot = %s"
        cursor.execute(query, (city, date, time_slot))
        if cursor.fetchone():
            return jsonify({'error': 'This date or time slot is already booked!'}), 400

        # Insert New Booking
        insert_query = """
            INSERT INTO bookings (name, email, phone, address, city, date, time_slot, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name, email, phone, address, city, date, time_slot, payment_method))
        connection.commit()

        return jsonify({'success': 'Booking confirmed!'})

    except Exception as e:
        # Return error in JSON format
        return jsonify({'error': str(e)}), 500

    finally:
        # Ensure the connection is closed, even if an error occurred
        if connection:
            connection.close()

# Route to Handle Message Form Submission
@app.route('/submit_message', methods=['POST'])
def submit_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    connection = None  # Initialize connection to ensure it's accessible in finally block

    try:
        # Connect to Database
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # Insert New Message
        insert_query = """
            INSERT INTO messages (name, email, message)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (name, email, message))
        connection.commit()

        return jsonify({'success': 'Message sent! Any reply from us will be sent to your email!'})

    except Exception as e:
        # Return error in JSON format
        return jsonify({'error': str(e)}), 500

    finally:
        # Ensure the connection is closed, even if an error occurred
        if connection:
            connection.close()

@app.route('/home')
def home():
    return render_template('frontpage.html')  # Home page HTML

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')  # Gallery page HTML

@app.route('/services')
def services():
    return render_template('services.html')  # Services page HTML

@app.route('/menu')
def menu():
    return render_template('menu.html') #Menu page HTML

@app.route('/contact')
def contact():
    return render_template('contact.html')  # Contact Us page HTML

@app.route('/book', methods=['GET'])
def booking_page():
    return render_template('bookings.html')  # Booking HTML page

if __name__ == '__main__':
    app.run(debug=True)
