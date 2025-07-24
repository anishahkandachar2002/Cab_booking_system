🚖 Cab Booking and Management System


 🙏 Acknowledgements

Thanks to Anand Sir for the opportunity to build this project and to PES University for the support and encouragement.

This is a Flask-based web application for managing a cab booking platform with role-based access for Admin, Driver, and User.

🌐 Live Demo: [https://anisha007420.pythonanywhere.com/](https://anisha007420.pythonanywhere.com/)  
🔑 Demo Login (Admin):  
- Username: `admin`  
- Password: `admin123`  



 ✅ Features

- 🧑‍💼 Admin: Manage drivers, users, bookings, and pricing  
- 🚗 Driver: Register and await approval  
- 🙋‍♂️ User: Register and login to the system  
- 🔐 Role-based login and dashboards  
- ✅ Flash messages and session handling  



 ⚙️ Setup Instructions

 1. 🔃 Clone the Repository

```bash
git clone https://github.com/your-username/cab_booking.git
cd cab_booking
```

 2. 🛠️ Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate     On Windows: venv\Scripts\activate
```

 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

 4. 🗃️ Setup MySQL Database

1. Open your MySQL client (e.g., phpMyAdmin, MySQL CLI, MySQL Workbench).  
2. Create a new database, for example:

```sql
CREATE DATABASE cab_booking;
```

3. Import the SQL file:

```sql
USE cab_booking;
-- Upload and execute your .sql file here
```

> 💡 You can use tools like phpMyAdmin or MySQL CLI to upload and run the SQL dump.

 5. 🔧 Configure Database Connection

Edit the `db_config.py` file with your own MySQL credentials:

```python
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='your_mysql_user',
        password='your_mysql_password',
        database='cab_booking'
    )
```

 6. 🚀 Run the App

```bash
python app.py
```

By default, the app will be available at:

```
http://127.0.0.1:5000/
```



 📂 Project Structure

```
.
├── app.py
├── db_config.py
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── register_user.html
│   └── register_driver.html
├── adminuser.py
├── admindriver.py
├── adminbookings.py
├── adminpricing.py
├── driverfull.py
├── userfull.py
├── auth_users.py
└── requirements.txt
```



 📌 Notes

 Drivers must be approved by the Admin before login is allowed.
 Sessions are used to track user roles and access.


![Login Page](https://github.com/anishahkandachar2002/Cab_booking_system/blob/main/login.png)






 🧑‍💻 Author

Developed by [ANISHA H KANDACHAR](https://github.com/anishahkandachar2002)
[Santosh Kumar PG](https://github.com/Santhoshkumar-123)
[Shreyas K C](https://github.com/kcshreyas)
