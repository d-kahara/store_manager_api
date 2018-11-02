from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

from flask import current_app
import psycopg2.extras as extras
import psycopg2

# Local Imports
from ..utils.db_helper import init_db
from instance.config import key as secret_key


class User():
    """This class contains the functions of the user model"""
    password = ''

    def __init__(self, password='pass', email='mail@mail.com', role='Attendant'):
        """initialize the user model"""

        User.password = generate_password_hash(password)
        self.email = email
        self.registered_on = datetime.now()
        self.role = role
        self.db = init_db()

    def save_user(self):
        """Saves User Object to Database"""

        new_user = dict(
            role=self.role.lower(),
            email=self.email.lower(),
            password=self.password,
            registered_on=self.registered_on
        )
        # check if user exists
        if self.check_if_user_exists(new_user['email']):
            raise Forbidden("User already exists.Please log in to continue.")

        curr = self.db.cursor()

        sql = """INSERT INTO users (role,email, registered_on, password) \
            VALUES ( %(role)s, %(email)s, %(registered_on)s, %(password)s);
            """
        curr.execute(sql, new_user)
        self.db.commit()
        curr.close()

    def check_if_user_exists(self, email):
        database = self.db
        curr = database.cursor()
        curr.execute("select * from users where email = (%s);", (email.lower(),))
        result = curr.fetchone()
        if result:
            return True
        return False

    def get_user_by_email(self, email):
        """return user from the db given an email"""
        if self.check_if_user_exists(email) == False:
            raise NotFound('User does not Exist.')
        curr = self.db.cursor(cursor_factory=extras.DictCursor)
        curr.execute(
            "SELECT * FROM users WHERE email = (%s);", (email,))
        rows = curr.fetchall()
        resp = []

        for row in rows:
            resp.append(dict(row))
        return resp

    def encode_jwt_token(self, email, role):
        """method to generate access token"""

        # Set up payload with an expiry date, issued at date and email claim
        try:
            payload = {
                'exp': datetime.now() + timedelta(days=2, seconds=25),
                'iat': datetime.now(),
                'sub': email,
                'role': role
            }

            return jwt.encode(
                payload,
                secret_key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def decode_jwt_token(self, jw_token):
        """method to decode the JSON web token"""

        try:
            payload = jwt.decode(jw_token, secret_key, algorithms=['HS256'])
            return payload

        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please sign in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please sign in again'

    def logout_user(self, token):
        """logs out a user by adding their token to the blacklist table"""
        conn = self.db
        curr = conn.cursor()
        sql = """
                INSERT INTO blacklist 
                VALUES (%(tokens)s) RETURNING tokens;
                """
        bad_token = dict(
            tokens=token
        )
        curr.execute(sql, bad_token)
        bad_token = curr.fetchone()[0]
        conn.commit()
        curr.close()
        return bad_token

    def update_role(self,role,email):
            """update the role given the user's email"""
            dbconn = self.db
            curr = dbconn.cursor(cursor_factory=extras.DictCursor)

            # check if product exists
            if not self.check_if_user_exists(email):
                raise Forbidden(
                    "User  does not exist.")
            try:
                curr.execute("UPDATE users SET role= %s WHERE email = %s RETURNING user_id,role,email",
                            (role,email,))
                rows = curr.fetchall()
                curr.close()
                dbconn.commit()
                resp = []

                for row in rows:
                    resp.append(dict(row))
                return resp
                
            except (Exception, psycopg2.DatabaseError) as error:
                response= dict(
                    status="Failed.",
                    Message=error
                )
                return response

    def get_all(self):
        """This function returns a list of all the users"""
        dbconn = self.db
        curr = dbconn.cursor(cursor_factory=extras.DictCursor)
        curr.execute("""SELECT user_id, role, email, registered_on FROM users;""")
        #returns a python dictionary like interface
        rows = curr.fetchall()
        resp = []

        for row in rows:
            resp.append(dict(row))
        return resp
