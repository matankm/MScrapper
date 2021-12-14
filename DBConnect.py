#
#

import mysql.connector



def db(query):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             port=3306,
                                             database='stage',
                                             user='mamur',
                                             password='TakieTamHaslo123')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            print("### COMMITTED ###")

    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")