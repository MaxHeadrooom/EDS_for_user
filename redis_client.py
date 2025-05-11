import redis
from functools import wraps
import pickle
# Инициализация клиента Redis, соединяющегося с локальным Docker-контейнером
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def test_connection():
    """
    Тестирует соединение с Redis и возвращает True, если успешное соединение.
    """
    try:
        return redis_client.ping()
    except redis.RedisError as e:

        print(f"Ошибка соединения с Redis: {e}")
        return False


def redis_cache(ttl: int = 60):
    """
    Декоратор для кеширования результатов функций в Redis с указанным TTL (в секундах).
    Ключ формируется из имени функции и её аргументов.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Формируем уникальный ключ для кэша
            key = f"{fn.__name__}:{args}:{sorted(kwargs.items())}"
            try:
                data = redis_client.get(key)
                if data:
                    # Если есть в кэше, возвращаем распакованный результат
                    return pickle.loads(data)
            except redis.RedisError:
                # При ошибке подключения просто выполняем функцию
                return fn(*args, **kwargs)

            # Иначе вычисляем результат и сохраняем в кэше
            result = fn(*args, **kwargs)
            try:
                redis_client.setex(key, ttl, pickle.dumps(result))
            except redis.RedisError:
                pass
            return result
        return wrapper
    return decorator

# Пример использования:
#
# @redis_cache(ttl=120)
# def get_heavy_report(user_id):
#     # Здесь ваш тяжёлый SQL-запрос к PostgreSQL
#     ...

if __name__ == '__main__':
    if test_connection():
        print("Redis connected: True")
    else:
        print("Redis connected: False")
