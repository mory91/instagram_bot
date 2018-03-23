# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime, time

def check_and_update(self):
    """ At the Program start, i does look for the sql updates """
    self.follows_db_c.execute('CREATE TABLE IF NOT EXISTS `usernames` ( `username` varchar ( 300 ), `my_username` varchar ( 300 ) );')
    self.follows_db_c.execute('CREATE TABLE IF NOT EXISTS `medias` (`media_id` varchar(300), `my_username` varchar(300));')
    table_info = self.follows_db_c.execute('DESC `medias`')
    table_column_status = [o for o in self.follows_db_c if o[0] == "status"]
    if not table_column_status:
        self.follows_db_c.execute("ALTER TABLE medias ADD COLUMN status integer")
    table_info = self.follows_db_c.execute("desc `medias`")
    table_column_status = [o for o in self.follows_db_c if o[0] == "datetime"]
    if not table_column_status:
        self.follows_db_c.execute("ALTER TABLE medias ADD COLUMN datetime TEXT")
    table_info = self.follows_db_c.execute("desc `medias`")
    table_column_status = [o for o in self.follows_db_c if o[0] == "code"]
    if not table_column_status:
        self.follows_db_c.execute("ALTER TABLE medias ADD COLUMN code TEXT")
    table_info = self.follows_db_c.execute("desc `usernames`")
    table_column_status = [o for o in self.follows_db_c if o[0] == "username_id"]
    if not table_column_status:
        qry = """
            CREATE TABLE `usernames_new` ( `username_id` varchar ( 300 ), `username` TEXT, `my_username` varchar ( 300 )  );
            INSERT INTO `usernames_new` (username_id) Select username from usernames;
            DROP TABLE `usernames`;
            ALTER TABLE `usernames_new` RENAME TO `usernames`;
              """
        self.follows_db_c.cmd_query_iter(qry)
    table_info = self.follows_db_c.execute("desc `usernames`")
    table_column_status = [o for o in self.follows_db_c if o[0] == "unfollow_count"]
    if not table_column_status:
        self.follows_db_c.execute("ALTER TABLE usernames ADD COLUMN unfollow_count INTEGER DEFAULT 0")
    table_info = self.follows_db_c.execute("desc `usernames`")
    table_column_status = [o for o in self.follows_db_c if o[0] == "last_followed_time"]
    if not table_column_status:
        self.follows_db_c.execute("ALTER TABLE usernames ADD COLUMN last_followed_time TEXT")
    self.follows_db_c.execute('SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME="settings";')
    table_info = self.follows_db_c.fetchone()
    if not table_info:
        qry = """
            CREATE TABLE `settings` ( `settings_name` TEXT, `settings_val` TEXT, `my_username` varchar ( 300 )  );
              """
        self.follows_db_c.execute(qry)
    #table_column_status = [o for o in table_info if o[1] == "last_followed_time"]
    #if not table_column_status:
    #    self.follows_db_c.execute("ALTER TABLE usernames ADD COLUMN last_followed_time TEXT")
    

def check_already_liked(self, media_id, username):
    """ controls if media already liked before """
    self.follows_db_c.execute("SELECT EXISTS(SELECT 1 FROM medias WHERE media_id='"+
                                 media_id + "' AND my_username='" + username + "' LIMIT 1)")
    fetchone_helper = self.follows_db_c.fetchone()
    if fetchone_helper[0] > 0:
        return 1
    return 0

def check_already_followed(self, user_id, username):
    """ controls if user already followed before """
    self.follows_db_c.execute("SELECT EXISTS(SELECT 1 FROM usernames WHERE username_id='"+
                                 user_id + "' AND my_username='" + username + "' LIMIT 1)")
    fetchone_helper = self.follows_db_c.fetchone()
    if fetchone_helper[0] > 0:
        return 1
    return 0

def insert_media(self, media_id, status, username):
    """ insert media to medias """
    now = datetime.now()
    self.follows_db_c.execute("INSERT INTO `medias` (media_id, status, datetime, my_username) VALUES('"+
                              media_id +"','"+ status +"','"+ str(now) +"','" + str(username) + "')")

def insert_username(self, user_id, username, my_username):
    """ insert user_id to usernames """
    now = datetime.now()
    self.follows_db_c.execute("INSERT INTO usernames (username_id, username, last_followed_time, my_username) \
                               VALUES('"+user_id+"','"+username+"','"+ str(now) + "','" + str(my_username) +"')")

def insert_unfollow_count(self, my_username, user_id=False, username=False):
    """ track unfollow count for new futures """
    if user_id:
        qry = "UPDATE usernames \
              SET unfollow_count = unfollow_count + 1 \
              WHERE username_id ='"+user_id+"'"
        self.follows_db_c.execute(qry)
    elif username:
        qry = "UPDATE usernames \
              SET unfollow_count = unfollow_count + 1 \
              WHERE username ='"+username+"' AND my_username='" + my_username + "'"
        self.follows_db_c.execute(qry)
    else:
        return False

def get_usernames_first(self, my_username):
    """ Gets first element of usernames table """
    username = self.follows_db_c.execute("SELECT * FROM usernames WHERE my_username='" + my_username + "' LIMIT 1")
    if username:
        return username
    else:
        return False

def get_usernames(self, my_username):
    """ Gets usernames table """
    usernames = self.follows_db_c.execute("SELECT * FROM usernames WHERE my_username='" + my_username + "' LIMIT 1")
    if usernames:
        return usernames
    else:
        return False

def get_username_random(self, my_username):
    """ Gets random username """
    self.follows_db_c.execute("SELECT * FROM usernames WHERE unfollow_count=0 AND my_username='" + my_username + "' ORDER BY RAND() LIMIT 1")
    username = self.follows_db_c.fetchone()
    if username:
        return username
    else:
        return False

def check_and_insert_user_agent(self, user_agent, my_username):
    """ Check user agent  """
    qry = "SELECT settings_val from settings where settings_name = 'USERAGENT' AND my_username='" + my_username + "' "
    self.follows_db_c.execute(qry)
    result_check = self.follows_db_c.fetchone()
    if result_check:
        result_get = result_check[0]
        return result_get
    else:
        qry_insert = """
                    INSERT INTO settings (settings_name, settings_val, my_username)
                    VALUES ('USERAGENT', '%s' , '%s')
                     """ % (user_agent, my_username)
        self.follows_db_c.execute(qry_insert)
        return check_and_insert_user_agent(self, user_agent, my_username)
