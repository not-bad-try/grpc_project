import psycopg2

# Параметры подключения к базе данных
DB_NAME = "grpc_db"
DB_USER = "grpc_user"
DB_PASSWORD = "grpc_pass"
DB_HOST = "localhost"

# Создание базы данных и таблицы
def create_database():
    try:
        # Подключение к PostgreSQL
        conn = psycopg2.connect(
            dbname="postgres", user="postgres", password="password", host=DB_HOST
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Создание базы данных
        cursor.execute(f"CREATE DATABASE {DB_NAME};")
        cursor.close()
        conn.close()

        # Подключение к новой базе данных для создания таблицы
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        cursor = conn.cursor()

        # Создание таблицы grpc_data
        cursor.execute("""
            CREATE TABLE grpc_data (
                PacketSeqNum INT,
                RecordSeqNum INT,
                PacketTimestamp TIMESTAMP,
                Decimal1 NUMERIC,
                Decimal2 NUMERIC,
                Decimal3 NUMERIC,
                Decimal4 NUMERIC,
                RecordTimestamp TIMESTAMP,
                PRIMARY KEY (PacketSeqNum, RecordSeqNum)
            );
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("База данных и таблица успешно созданы!")

    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")

if __name__ == '__main__':
    create_database()
