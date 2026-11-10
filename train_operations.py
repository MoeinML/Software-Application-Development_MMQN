from db import get_connection

def get_all_trains():
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            "SELECT * FROM train ORDER BY train_id"
        )
        trains = cursor.fetchall()
        return trains
    
    finally:
        cursor.close()
        connection.close()