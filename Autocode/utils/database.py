#
#   Database utilities
#   Created on 2018-01-06

#   from pkg_resources      import resource_string
from sqlite3 import connect, Error
from FileItem import FileItem

#   resource_string('resources.database', "Autocode.sqlite3")
__SQL_DB_FILE__ = "Autocode.sqlite3"


__SQL_INSERT__ = "INSERT INTO processed_file (file_name, file_path, file_size, file_status, start_time) " \
                 "VALUES(?, ?, ?, ?, ?);"

__SQL_UPDATE__ = "UPDATE processed_file SET encoded_file_name = ?, encoded_file_path = ?, encoded_file_size = ?, " \
                 "codec = ?, finish_time = ?, file_status = ? WHERE file_name = ? AND file_path = ? and " \
                 "file_status != ?;"

__SQL_SELECT__ = "SELECT file_name, file_path, file_size, file_status, start_time, finish_time, " \
                 "encoded_file_name, encoded_file_path, encoded_file_size, codec " \
                 "FROM processed_file " \
                 "WHERE file_name = ? and file_path = ?"


def create_connection():
    """ creates a database connection to the autocode SQLite database
    :return: Connection object or None
    """

    try:
        conn = connect(__SQL_DB_FILE__)
        return conn
    except Error as e:
        print(e)

    return None


def find_file(file_item):
    """
    Finds the file in the database
    :param file_item:
    :return: the file_item present in the database
    """
    conn = create_connection()
    with conn:
        cursor = conn.execute(__SQL_SELECT__, (file_item.file_name, file_item.file_path))
        return [FileItem.from_db(*row) for row in cursor.fetchall()]


def insert_file(file_item):
    """Inserts a file into the autocode database
    :param file_item: the file item to insert
    :return:
    """
    conn = create_connection()
    with conn:
        __insert_file(conn, file_item)


def update_file(file_item):
    """Updates a file which is present in the autocode database
    :param file_item: the file item to update
    :return:
    """
    conn = create_connection()
    with conn:
        __update_file(conn, file_item)


def __insert_file(connection, file_item):
    """
    Inserts a file into the autocode database
    :param connection:
    :param file_item: the FileItem to insert
    :return:
    """
    cursor = connection.cursor()
    cursor.execute(__SQL_INSERT__, (file_item.file_name, file_item.file_path, file_item.file_size,
                                    file_item.file_status, file_item.start_time))
    connection.commit()


def __update_file(connection, file_item):
    """
    Inserts a file into the autocode database
    :param connection:
    :param file_item: the FileItem to insert
    :return:
    """
    cursor = connection.cursor()
    cursor.execute(__SQL_UPDATE__, (file_item.encoded_file_name, file_item.encoded_file_path,
                                    file_item.encoded_file_size, file_item.codec, file_item.end_time,
                                    file_item.file_status, file_item.file_name, file_item.file_path,
                                    file_item.file_status))
    connection.commit()


def test_connection():
    item = FileItem("NAME", "PATH", 123)
    #   insert_file(item)

    # item.set_started("OP FILE PATH", "OP FILE NAME", "PASS THRU")
    print find_file(item)


if __name__ == '__main__':
    test_connection()

# __SQL_TABLE_TEST__ = "SELECT name FROM sqlite_master WHERE type='table' and name='processed_file';"
# __SQL_TABLE_CREATE__ =             \
#     "CREATE TABLE processed_file (          \
#         file_name     varchar(500),         \
#         file_path     varchar(500),         \
#         start_time    timestamp,            \
#         finish_time   timestamp,            \
#         codec         varchar(500),         \
#         status        varchar(20),          \
#         primary key(file_name, file_path)   \
#     );"
#
# def open_database():
#     """Opens a connection to the Autocdode database
#     :return: the connection or none if the database cant be opened.
#     """
#     #   Create a connection
#     connection = create_connection()
#
#     #   Test if the table exists
#     cursor = connection.cursor()
#     cursor.execute(__SQL_TABLE_TEST__)
#
#     #   if it does not, create the table
#     if len(cursor.fetchall()) == 0:
#         print("Creating a table to store files")
#         cursor.execute(__SQL_TABLE_TEST__)
#         connection.commit()
#
#     #   return the connection
#     return connection
