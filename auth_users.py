from db_config import get_connection

class BaseUser:
    def __init__(self, userid, password):
        self.userid = userid
        self.password = password
        self.role = None
        self.user_data = None

    def connect_db(self):
        conn = get_connection()
        return conn.cursor(dictionary=True), conn

    def authenticate(self):
        raise NotImplementedError("Subclasses must implement this method")

    def is_authenticated(self):
        return self.user_data is not None


class AdminUser(BaseUser):
    def __init__(self, userid, password):
        super().__init__(userid, password)
        self.role = 'admin'

    def authenticate(self):
        cursor, conn = self.connect_db()
        cursor.execute("SELECT * FROM admin_users WHERE username=%s AND password=%s", (self.userid, self.password))
        self.user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        return self.user_data


class DriverUser(BaseUser):
    def __init__(self, userid, password):
        super().__init__(userid, password)
        self.role = 'driver'

    def authenticate(self):
        cursor, conn = self.connect_db()
        cursor.execute("SELECT * FROM drivers WHERE user_id=%s AND password=%s", (self.userid, self.password))
        driver = cursor.fetchone()
        if driver and driver['approved'] == 1:
            self.user_data = driver
        cursor.close()
        conn.close()
        return self.user_data


class RegularUser(BaseUser):
    def __init__(self, userid, password):
        super().__init__(userid, password)
        self.role = 'user'

    def authenticate(self):
        cursor, conn = self.connect_db()
        cursor.execute("SELECT * FROM users WHERE user_id=%s AND password=%s", (self.userid, self.password))
        self.user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        return self.user_data
