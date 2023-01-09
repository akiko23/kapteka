import random
import sqlite3
import string


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.Connection(db_file)
        self.cursor = self.connection.cursor()

    def request_to_database(self, request, *args):
        with self.connection:
            return self.cursor.execute(request, *args)

    def add_user(self, user_id):
        self.request_to_database("INSERT INTO bot_user (user_id, money) VALUES (?, 0)", (user_id,))

    def user_exists(self, user_id):
        res = self.request_to_database("SELECT `user_id` FROM bot_user WHERE user_id=?", (user_id,)).fetchall()
        return bool(len(res))

    def create_product(self, cat):
        self.request_to_database("INSERT INTO bot_product (category) VALUES (?)", (cat,))

    def set_something(self, param_to_set, value_to_set):
        uid = self.get_last_id()
        self.request_to_database(f'UPDATE bot_product SET {param_to_set}=? WHERE id=?',
                                 (value_to_set, uid,))

    def get_last_id(self):
        return self.request_to_database("SELECT id FROM bot_product").fetchall()[-1][
            0]

    def get_all_products_data(self):
        uid = self.get_last_id()
        return self.request_to_database("SELECT id, photo_id, name, description, price FROM bot_product WHERE id=?",
                                        (uid,)).fetchall()

    def delete_advertisement(self, user_id, unique_id):
        self.request_to_database("DELETE FROM bot_product WHERE id=?", (unique_id,))

    def get_all_categories(self):
        return set([i[0] for i in self.request_to_database(f"SELECT name FROM bot_category").fetchall()])

    def get_products_by_category(self, category):
        return self.request_to_database(
            "SELECT id, photo_id, name, description, price FROM bot_product WHERE category=?",
            (category,)).fetchall()

    def get_all_category_ids(self):
        return [i[0] for i in self.request_to_database("SELECT id FROM bot_category").fetchall()]

    def add_category(self, cat):
        self.request_to_database("INSERT INTO bot_category (name) VALUES (?)", (cat,))

    def set_inviter_id(self, user_id, inviter_id):
        self.request_to_database("UPDATE bot_user SET inviter_id=? WHERE user_id=?", (inviter_id, user_id,))

    def get_invited_users(self, user_id):
        try:
            return self.request_to_database("SELECT invited_users FROM bot_user WHERE user_id=?", (user_id,)).fetchall()[0][
                0].strip()
        except AttributeError:
            return ''

    def update_invited_users(self, user_id, inviter_id):
        invited_users = self.get_invited_users(inviter_id).split()
        invited_users.append(str(user_id))

        self.request_to_database("UPDATE bot_user SET invited_users=? WHERE user_id=?",
                                 (" ".join(invited_users), inviter_id,))

    def get_ref_percent(self):
        return self.request_to_database("SELECT percent FROM bot_refpercent").fetchone()[0]

# db = Database('db.sqlite3')
# db.set_inviter_id(5132067462, 818525681)
