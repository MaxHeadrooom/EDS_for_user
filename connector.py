import threading
from queue import Queue
from contextlib import contextmanager
import pg8000
from settings import DB_CONFIG, POOL_MIN_CONN, POOL_MAX_CONN
import atexit

class SimpleConnectionPool:
    """Реализация простого пула подключений для pg8000."""
    def __init__(self, min_conn, max_conn, **db_config):
        self.db_config = db_config
        self.lock = threading.Lock()
        self.pool = Queue(max_conn)

        # Инициализация минимального числа соединений
        print("Initializing connection pool...")
        for _ in range(min_conn):
            self.pool.put(self.create_connection())

    def create_connection(self):
        """Создает новое соединение с базой данных."""
        return pg8000.connect(**self.db_config)

    def getconn(self):
        """Получает соединение из пула."""
        with self.lock:
            if self.pool.empty():
                print("No available connections in pool. Creating a new one.")
                return self.create_connection()
            return self.pool.get()

    def putconn(self, connection):
        """Возвращает соединение в пул."""
        with self.lock:
            if not self.pool.full():
                self.pool.put(connection)
            else:
                print("Connection pool is full. Closing the connection.")
                connection.close()

    def closeall(self):
        """Закрывает все соединения в пуле."""
        with self.lock:
            while not self.pool.empty():
                conn = self.pool.get()
                conn.close()
            print("All connections closed.")


# Инициализируем пул подключений
connection_pool = SimpleConnectionPool(POOL_MIN_CONN, POOL_MAX_CONN, **DB_CONFIG)


@contextmanager
def get_connection():
    """Контекстный менеджер для работы с соединениями из пула."""
    connection = connection_pool.getconn()
    try:
        yield connection
    finally:
        connection_pool.putconn(connection)


def close_connection_pool():
    """Закрывает все соединения в пуле."""
    if connection_pool:
        connection_pool.closeall()
        print("Connection pool closed.")


def on_exit():
    """Действия при завершении программы."""
    print("Приложение завершено! Закрываем ресурсы...")
    close_connection_pool()


# Регистрируем функцию для выполнения при завершении программы
atexit.register(on_exit)

# Пример использования
if __name__ == "__main__":
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            print(f"Query result: {cursor.fetchone()}")
    except Exception as e:
        print(f"Error occurred: {e}")
