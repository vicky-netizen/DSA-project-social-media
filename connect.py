import mysql.connector

def main():

    db_connection =mysql.connector.connect(host='localhost',user='root',password='root',database='dsa')

    # Create cursor
    cursor = db_connection.cursor()

    # Fetch data from MySQL table
    cursor.execute("SELECT User, Friend FROM userFriends")
    rows = cursor.fetchall()

    # Print the table content
    print("User\tFriend")
    for row in rows:
        print(f"{row[0]}\t{row[1]}")

    # Close cursor and database connection
    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    main()
