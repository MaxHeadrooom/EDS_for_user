import os
import time
import hashlib
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from connector import get_connection
from pandas import DataFrame
import pandas as pd

load_dotenv("env.env")

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(input_password, stored_hash):
    return hash_password(input_password) == stored_hash

def registration():
    st.title("Регистрация")

    # Поля для ввода данных регистрации
    reg_name = st.text_input("Введите логин", key="reg_name")
    reg_password = st.text_input("Введите пароль", type="password", key="reg_password")
    reg_email = st.text_input("Введите email", key="reg_email")
    fio = st.text_input("Введите ваше ФИО", key="fio")

    # Кнопка для завершения регистрации
    if st.button("Зарегистрироваться"):
        if reg_name and reg_password and reg_email and fio:
            try:
                with get_connection() as conn:
                    cursor = conn.cursor()

                    # Проверяем существование пользователя с таким логином или email
                    cursor.execute(
                        'SELECT id FROM db.users WHERE username = %s OR email = %s',
                        (reg_name, reg_email)
                    )
                    existing_user = cursor.fetchone()

                    if existing_user:
                        st.error("Пользователь с таким логином или email уже существует")
                    else:
                        # Генерация хэша пароля
                        hashed_password = hash_password(reg_password)

                        # Получаем максимальный id из таблицы users
                        cursor.execute('SELECT COALESCE(MAX(id), 0) FROM db.users')
                        last_id = cursor.fetchone()[0]

                        # Вставляем нового пользователя
                        cursor.execute(
                            '''
                            INSERT INTO db.users ("id", "username", "password_hash", "email", "full_name", "created_at", "level") 
                            VALUES (%s, %s, %s, %s, %s, now(), %s)
                            ''',
                            (last_id + 1, reg_name, hashed_password, reg_email, fio, 1)  # level = 1 (обычный пользователь)
                        )
                        conn.commit()
                        st.success("Регистрация прошла успешно! Теперь вы можете войти.")
                        time.sleep(2)
                        # Переключение обратно на страницу входа
                        st.session_state["current_page"] = "login"
                        st.session_state["rerun"] = True  # Скрытый триггер для обновления
            except Exception as e:
                print(f"Error occurred: {e}")
        else:
            st.error("Заполните все поля!")

def login():
    st.title("Вход в аккаунт")

    log_name = st.text_input("Введите логин", key="log_name")
    log_password = st.text_input("Введите пароль", type="password", key="log_password")

    if st.button("Войти"):
        if log_name and log_password:
            try:
                with get_connection() as conn:
                    cursor = conn.cursor()

                    # Извлекаем ID, хэш пароля и уровень пользователя
                    cursor.execute(
                        'SELECT id, password_hash, level FROM db.users WHERE username = %s',
                        (log_name,)
                    )
                    user_data = cursor.fetchone()

                    if user_data:
                        user_id, stored_hashed_password, user_level = user_data

                        if verify_password(log_password, stored_hashed_password):
                            st.success(f"Добро пожаловать, {log_name}! Ваш уровень: {user_level}")

                            time.sleep(2)

                            # Сохраняем данные в сессии
                            st.session_state["current_page"] = "come_mess"
                            st.session_state["user_level"] = user_level
                            st.session_state["id"] = user_id
                            st.session_state["rerun"] = True
                        else:
                            st.error("Неверный пароль.")
                    else:
                        st.error("Пользователь с таким логином не найден.")
            except Exception as e:
                print(f"Error occurred: {e}")
        else:
            st.error("Введите логин и пароль!")


    # Кнопка для перехода на страницу регистрации
    if st.button("Зарегистрироваться"):
        st.session_state["current_page"] = "registration"
        st.session_state["rerun"] = True  # Скрытый триггер для обновления

def add_vhod_doc():
    st.title("Введите данные")

    # Получаем ID текущего пользователя из сессии
    id = st.session_state.get("id")

    # Поля для ввода данных
    date = st.text_input("Дата (в формате YYYY-MM-DD)", key="date")
    number = st.text_input("Номер", key="number")
    st.text("Получен от")
    second_name = st.text_input("Фамилия", key="second_name")
    first_name = st.text_input("Имя", key="name")
    last_name = st.text_input("Отчество", key="last_name")

    # Кнопка для добавления документа
    if st.button("Добавить"):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Проверяем, существует ли уже "Получен от" (writer) в базе данных
                cursor.execute(
                    'SELECT COALESCE(id, 0) FROM db."Лицо" WHERE "Фамилия" = %s and "Имя" = %s and "Отчество" = %s',
                    (second_name, first_name, last_name)
                )
                result = cursor.fetchone()

                # Устанавливаем id_writer на значение ID или 0, если writer отсутствует
                pisal = result[0] if result else 0

                if pisal == 0:
                    cursor.execute('SELECT COALESCE(MAX(id), 0) FROM db."Лицо"')
                    last_id = cursor.fetchone()[0]
                    cursor.execute(
                        '''
                        INSERT INTO db."Лицо" ("id", "Фамилия", "Имя", "Отчество", "Телефон", "e-mail", "Должность", "Работает в") 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ''',
                        (last_id + 1, second_name, first_name, last_name, 'Null', 'Null', 0, 0)
                    )
                    id_writer = last_id + 1
                else:
                    id_writer = pisal

                # Генерируем новый ID для документа
                cursor.execute('SELECT COALESCE(MAX(id), 0) FROM db."Входящий документ"')
                last_id = cursor.fetchone()[0] + 1

                # Вставляем новый документ в базу данных
                cursor.execute(
                    '''
                    INSERT INTO db."Входящий документ"("id", "Дата", "Номер", "Получен от", "user_id", "Получен_от_организация")
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ''',
                    (last_id, date, number, id_writer, id, 0)
                )
                conn.commit()
                st.success("Документ успешно добавлен")

                # Переход на другую страницу после успешного добавления
                time.sleep(2)
                st.session_state["current_page"] = "add_doc"
                st.session_state["rerun"] = True  # Триггер для перерисовки страницы
        except Exception as e:
            st.error("Произошла ошибка при добавлении документа")
            print(f"Error occurred: {e}")

def add_vhod_doc_org():
    st.title("Введите данные")

    # Получаем ID текущего пользователя из сессии
    id = st.session_state.get("id")

    # Поля для ввода данных
    date = st.text_input("Дата (в формате YYYY-MM-DD)", key="date")
    number = st.text_input("Номер", key="number")
    st.text("Получен от")
    inn_of_org = st.text_input("ИНН", key="inn_of_org")
    name_of_org = st.text_input("Полное название организации", key="name_of_org")
    short_name_of_org = st.text_input("Краткое название организации", key="short_name_of_org")

    # Кнопка для добавления документа
    if st.button("Добавить"):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                if not (inn_of_org or name_of_org or short_name_of_org):
                    st.error("Заполните хотя бы одно поле об организации.")
                    return

                if inn_of_org:
                    cursor.execute('SELECT COALESCE(id, 0) FROM db."Организация" WHERE "ИНН" = %s', (inn_of_org,))
                elif name_of_org:
                    cursor.execute('SELECT COALESCE(id, 0) FROM db."Организация" WHERE "Полное наименование" = %s',
                                   (name_of_org,))
                else:
                    cursor.execute('SELECT COALESCE(id, 0) FROM db."Организация" WHERE "Краткое наименование" = %s',
                                   (short_name_of_org,))

                result = cursor.fetchone()

                # Устанавливаем id_writer на значение ID или 0, если writer отсутствует
                pisal = result[0] if result else 0

                if inn_of_org == '':
                    inn_of_org = 0

                if pisal == 0:
                    cursor.execute('SELECT COALESCE(MAX(id), 0) FROM db."Организация"')
                    last_id = cursor.fetchone()[0]

                    cursor.execute(
                        '''
                        INSERT INTO db."Организация" ("id", "Полное наименование", "Краткое наименование", "ОГРН", "ИНН", "Адрес юридический", "Адрес фактический", "Адрес почтовый", "Телефон", "e-mail", "Руководитель") 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ''',
                        (last_id + 1, name_of_org, short_name_of_org, 1, inn_of_org, 1, 1, 1, 'Null', 'Null', 0)
                    )

                    id_writer = last_id + 1
                else:
                    id_writer = pisal

                # Генерируем новый ID для документа
                cursor.execute('SELECT COALESCE(MAX(id), 0) FROM db."Входящий документ"')
                last_id = cursor.fetchone()[0] + 1

                # Вставляем новый документ в базу данных
                cursor.execute(
                    '''
                    INSERT INTO db."Входящий документ"("id", "Дата", "Номер", "Получен от", "user_id", "Получен_от_организация")
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ''',
                    (last_id, date, number, 0, id, id_writer)
                )
                conn.commit()
                st.success("Документ успешно добавлен")

                # Переход на другую страницу после успешного добавления
                time.sleep(2)
                st.session_state["current_page"] = "add_doc"
                st.session_state["rerun"] = True  # Триггер для перерисовки страницы
        except Exception as e:
            st.error("Произошла ошибка при добавлении документа")
            print(f"Error occurred: {e}")

def phys_or_org():
    st.title("Выбор отправителя")

    if (st.button("Физическое лицо")):
        st.session_state["current_page"] = "add_vhod_doc"
        st.session_state["rerun"] = True

    if (st.button("Организация")):
        st.session_state["current_page"] = "add_vhod_doc_org"
        st.session_state["rerun"] = True

    if (st.button("Назад")):
        st.session_state["current_page"] = "add_doc"
        st.session_state["rerun"] = True

def add_lic():
    st.title("Введите данные")

    # Получаем ID текущего пользователя из сессии
    id = st.session_state.get("id")

    # Поля для ввода данных
    date = st.text_input("Дата (в формате YYYY-MM-DD)", key="date")
    number = st.text_input("Номер", key="number")
    st.text("Направлен")
    second_name = st.text_input("Фамилия", key="second_name")
    first_name = st.text_input("Имя", key="name")
    last_name = st.text_input("Отчество", key="last_name")

    # Кнопка для добавления документа
    if st.button("Добавить"):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Проверяем, существует ли уже "Получен от" (writer) в базе данных
                cursor.execute(
                    'SELECT COALESCE(id, 0) FROM db."Лицо" WHERE "Фамилия" = %s and "Имя" = %s and "Отчество" = %s',
                    (second_name, first_name, last_name)
                )
                result = cursor.fetchone()

                # Устанавливаем id_writer на значение ID или 0, если writer отсутствует
                pisal = result[0] if result else 0

                if pisal == 0:
                    cursor.execute('SELECT COALESCE(MAX(id), 0) FROM db."Лицо"')
                    last_id = cursor.fetchone()[0]
                    cursor.execute(
                        '''
                        INSERT INTO db."Лицо" ("id", "Фамилия", "Имя", "Отчество", "Телефон", "e-mail", "Должность", "Работает в") 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ''',
                        (last_id + 1, second_name, first_name, last_name, 'Null', 'Null', 0, 0)
                    )
                    id_writer = last_id + 1
                else:
                    id_writer = pisal

                # Генерируем новый ID для документа
                cursor.execute('SELECT COALESCE(MAX(id), 0) FROM db."Исходящий документ"')
                last_id = cursor.fetchone()[0] + 1

                # Вставляем новый документ в базу данных
                cursor.execute(
                    '''
                    INSERT INTO db."Исходящий документ"("id", "Дата", "Номер", "Направлен", "user_id", "Направлен_организация")
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ''',
                    (last_id, date, number, id_writer, id, 0)
                )
                conn.commit()
                st.success("Документ успешно добавлен")

                # Переход на другую страницу после успешного добавления
                time.sleep(2)
                st.session_state["current_page"] = "add_doc"
                st.session_state["rerun"] = True  # Триггер для перерисовки страницы
        except Exception as e:
            st.error("Произошла ошибка при добавлении документа")
            print(f"Error occurred: {e}")

def add_org():
    st.title("Введите данные")

    # Получаем ID текущего пользователя из сессии
    id = st.session_state.get("id")

    # Поля для ввода данных
    date = st.text_input("Дата (в формате YYYY-MM-DD)", key="date")
    number = st.text_input("Номер", key="number")
    st.text("Направлен")
    inn_of_org = st.text_input("ИНН", key="inn_of_org")
    name_of_org = st.text_input("Полное название организации", key="name_of_org")
    short_name_of_org = st.text_input("Краткое название организации", key="short_name_of_org")

    # Кнопка для добавления документа
    if st.button("Добавить"):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()



                if not (inn_of_org or name_of_org or short_name_of_org):
                    st.error("Заполните хотя бы одно поле об организации.")
                    return

                if inn_of_org:
                    cursor.execute('SELECT COALESCE(id, 0) FROM db."Организация" WHERE "ИНН" = %s', (inn_of_org,))
                elif name_of_org:
                    cursor.execute('SELECT COALESCE(id, 0) FROM db."Организация" WHERE "Полное наименование" = %s',
                                   (name_of_org,))
                else:
                    cursor.execute('SELECT COALESCE(id, 0) FROM db."Организация" WHERE "Краткое наименование" = %s',
                                   (short_name_of_org,))

                result = cursor.fetchone()

                # Устанавливаем id_writer на значение ID или 0, если writer отсутствует
                pisal = result[0] if result else 0

                if inn_of_org == '':
                    inn_of_org = 0

                if pisal == 0:
                    cursor.execute('SELECT COALESCE(MAX(id), 0) FROM db."Организация"')
                    last_id = cursor.fetchone()[0]

                    cursor.execute(
                        '''
                        INSERT INTO db."Организация" ("id", "Полное наименование", "Краткое наименование", "ОГРН", "ИНН", "Адрес юридический", "Адрес фактический", "Адрес почтовый", "Телефон", "e-mail", "Руководитель") 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ''',
                        (last_id + 1, name_of_org, short_name_of_org, 1, inn_of_org, 1, 1, 1, 'Null', 'Null', 0)
                    )

                    id_writer = last_id + 1
                else:
                    id_writer = pisal

                # Генерируем новый ID для документа
                cursor.execute('SELECT COALESCE(MAX(id), 0) FROM db."Исходящий документ"')
                last_id = cursor.fetchone()[0] + 1

                # Вставляем новый документ в базу данных
                cursor.execute(
                    '''
                    INSERT INTO db."Исходящий документ"("id", "Дата", "Номер", "Направлен", "user_id", "Направлен_организация")
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ''',
                    (last_id, date, number, 0, id, id_writer)
                )
                conn.commit()
                st.success("Документ успешно добавлен")

                # Переход на другую страницу после успешного добавления
                time.sleep(2)
                st.session_state["current_page"] = "add_doc"
                st.session_state["rerun"] = True  # Триггер для перерисовки страницы
        except Exception as e:
            st.error("Произошла ошибка при добавлении документа")
            print(f"Error occurred: {e}")

def send_doc():
    st.title("Выбор отправителя")

    if (st.button("Физическое лицо")):
        st.session_state["current_page"] = "add_lic"
        st.session_state["rerun"] = True

    if (st.button("Организация")):
        st.session_state["current_page"] = "add_org"
        st.session_state["rerun"] = True

    if (st.button("Назад")):
        st.session_state["current_page"] = "add_doc"
        st.session_state["rerun"] = True

def add_doc():
    st.title("Добавление нового документа")

    if (st.button("Входящий документ")):
        st.session_state["current_page"] = "phys_or_org"
        st.session_state["rerun"] = True

    if (st.button("Исходящий документ")):
        st.session_state["current_page"] = "send_doc"
        st.session_state["rerun"] = True

    if (st.button("Назад")):
        st.session_state["current_page"] = "come_mess"
        st.session_state["rerun"] = True

def ischod():
    id = st.session_state.get("id")

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    d."Дата", 
                    d."Номер", 
                    CONCAT(л."Фамилия", ' ', л."Имя", ' ', COALESCE(л."Отчество", '')) AS "ФИО", 
                    COALESCE(CAST(o."ИНН" AS TEXT), 'Не указано') AS "ИНН", 
                    COALESCE(o."Полное наименование", 'Не указано') AS "Полное название", 
                    COALESCE(o."Краткое наименование", 'Не указано') AS "Краткое название", 
                    'Исходящий' AS "Тип документа"
                FROM db."Исходящий документ" d
                LEFT JOIN db."Организация" o ON d."Направлен_организация" = o.id
                LEFT JOIN db."Лицо" л ON d."Направлен" = л.id
                WHERE d.user_id = %s;
            ''', (id,))

            results = cursor.fetchall()

            if results:
                st.write("Результаты запроса:")

                # Обработка результатов
                processed_results = []
                for row in results:
                    date, number, fio, inn, full_name, short_name, doc_type = row

                    fio = fio if fio != 'Мнимый Мнимый Мнимый' else '==========================>'
                    inn = inn if inn and inn != '0' else '<Не указано>'
                    full_name = full_name if full_name and full_name != 'Мнимый' else '<Не указано>'
                    short_name = short_name if short_name and short_name != 'Мнимый' else '<Не указано>'

                    # Добавляем строку в обработанные результаты
                    processed_results.append((date, number, fio, inn, full_name, short_name, doc_type))

                # Создание DataFrame
                df = pd.DataFrame(
                    processed_results,
                    columns=["Дата", "Номер", "ФИО", "ИНН", "Полное наименование", "Краткое название", "Тип документа"]
                )
                df.reset_index(drop=True, inplace=True)

                # Отображение таблицы
                st.dataframe(df.style.hide(axis="index"))
            else:
                st.write("Нет данных для указанного пользователя.")
    except Exception as e:
        st.error(f"Произошла ошибка: {e}")

    if (st.button("Назад")):
        st.session_state["current_page"] = "come_mess"
        st.session_state["rerun"] = True

def vhod():
    id = st.session_state.get("id")

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT 
                    d."Дата", 
                    d."Номер", 
                    CONCAT(л."Фамилия", ' ', л."Имя", ' ', COALESCE(л."Отчество", '')) AS "ФИО", 
                    COALESCE(CAST(o."ИНН" AS TEXT), 'Не указано') AS "ИНН", 
                    COALESCE(o."Полное наименование", 'Не указано') AS "Полное название", 
                    COALESCE(o."Краткое наименование", 'Не указано') AS "Краткое название", 
                    'Входящий' AS "Тип документа"
                FROM db."Входящий документ" d
                LEFT JOIN db."Организация" o ON d."Получен_от_организация" = o.id
                LEFT JOIN db."Лицо" л ON d."Получен от" = л.id
                WHERE d.user_id = %s
                ''', (id,))

            results = cursor.fetchall()

            if results:
                st.write("Результаты запроса:")

                # Обработка результатов
                processed_results = []
                for row in results:
                    date, number, fio, inn, full_name, short_name, doc_type = row

                    fio = fio if fio != 'Мнимый Мнимый Мнимый' else '==========================>'
                    inn = inn if inn and inn != '0' else '<Не указано>'
                    full_name = full_name if full_name and full_name != 'Мнимый' else '<Не указано>'
                    short_name = short_name if short_name and short_name != 'Мнимый' else '<Не указано>'

                    # Добавляем строку в обработанные результаты
                    processed_results.append((date, number, fio, inn, full_name, short_name, doc_type))

                # Создание DataFrame
                df = pd.DataFrame(
                    processed_results,
                    columns=["Дата", "Номер", "ФИО", "ИНН", "Полное наименование", "Краткое название", "Тип документа"]
                )
                df.reset_index(drop=True, inplace=True)

                # Отображение таблицы
                st.dataframe(df.style.hide(axis="index"))
            else:
                st.write("Нет данных для указанного пользователя.")
    except Exception as e:
        st.error(f"Произошла ошибка: {e}")

    if (st.button("Назад")):
        st.session_state["current_page"] = "come_mess"
        st.session_state["rerun"] = True

def vse_pol():
    id = st.session_state.get("id")  # Получение ID пользователя из сессии

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    d."Дата", 
                    d."Номер", 
                    CONCAT(л."Фамилия", ' ', л."Имя", ' ', COALESCE(л."Отчество", '')) AS "ФИО", 
                    COALESCE(CAST(o."ИНН" AS TEXT), 'Не указано') AS "ИНН", 
                    COALESCE(o."Полное наименование", 'Не указано') AS "Полное название", 
                    COALESCE(o."Краткое наименование", 'Не указано') AS "Краткое название", 
                    'Входящий' AS "Тип документа"
                FROM db."Входящий документ" d
                LEFT JOIN db."Организация" o ON d."Получен_от_организация" = o.id
                LEFT JOIN db."Лицо" л ON d."Получен от" = л.id
                WHERE d.user_id = %s
                
                UNION ALL
                
                SELECT 
                    d."Дата", 
                    d."Номер", 
                    CONCAT(л."Фамилия", ' ', л."Имя", ' ', COALESCE(л."Отчество", '')) AS "ФИО", 
                    COALESCE(CAST(o."ИНН" AS TEXT), 'Не указано') AS "ИНН", 
                    COALESCE(o."Полное наименование", 'Не указано') AS "Полное название", 
                    COALESCE(o."Краткое наименование", 'Не указано') AS "Краткое название", 
                    'Исходящий' AS "Тип документа"
                FROM db."Исходящий документ" d
                LEFT JOIN db."Организация" o ON d."Направлен_организация" = o.id
                LEFT JOIN db."Лицо" л ON d."Направлен" = л.id
                WHERE d.user_id = %s;
            ''', (id, id))

            results = cursor.fetchall()

            if results:
                st.write("Результаты запроса:")

                # Обработка результатов
                processed_results = []
                for row in results:
                    date, number, fio, inn, full_name, short_name, doc_type = row

                    fio = fio if fio != 'Мнимый Мнимый Мнимый' else '==========================>'
                    inn = inn if inn and inn != '0' else '<Не указано>'
                    full_name = full_name if full_name and full_name != 'Мнимый' else '<Не указано>'
                    short_name = short_name if short_name and short_name != 'Мнимый' else '<Не указано>'

                    # Добавляем строку в обработанные результаты
                    processed_results.append((date, number, fio, inn, full_name, short_name, doc_type))

                # Создание DataFrame
                df = pd.DataFrame(
                    processed_results,
                    columns=["Дата", "Номер", "ФИО", "ИНН", "Полное наименование", "Краткое название", "Тип документа"]
                )
                df.reset_index(drop=True, inplace=True)

                # Отображение таблицы
                st.dataframe(df.style.hide(axis="index"))
            else:
                st.write("Нет данных для указанного пользователя.")
    except Exception as e:
        st.error("Произошла ошибка при выполнении запроса.")
        print(f"Error occurred: {e}")

    if (st.button("Назад")):
        st.session_state["current_page"] = "come_mess"
        st.session_state["rerun"] = True

def vse_pol_admin():
    id = st.session_state.get("id")  # Получение ID пользователя из сессии

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    d."Дата", 
                    d."Номер", 
                    CONCAT(л."Фамилия", ' ', л."Имя", ' ', COALESCE(л."Отчество", '')) AS "ФИО",
                    COALESCE(u."username", 'Не указано') AS "Имя Пользователя",
                    COALESCE(CAST(o."ИНН" AS TEXT), 'Не указано') AS "ИНН", 
                    COALESCE(o."Полное наименование", 'Не указано') AS "Полное название", 
                    COALESCE(o."Краткое наименование", 'Не указано') AS "Краткое название", 
                    'Входящий' AS "Тип документа"
                FROM db."Входящий документ" d
                LEFT JOIN db."Организация" o ON d."Получен_от_организация" = o.id
                LEFT JOIN db."Лицо" л ON d."Получен от" = л.id
                LEFT JOIN db."users" u ON d."user_id" = u.id

                UNION ALL

                SELECT 
                    d."Дата", 
                    d."Номер", 
                    CONCAT(л."Фамилия", ' ', л."Имя", ' ', COALESCE(л."Отчество", '')) AS "ФИО",
                    COALESCE(u."username", 'Не указано') AS "Имя Пользователя",
                    COALESCE(CAST(o."ИНН" AS TEXT), 'Не указано') AS "ИНН", 
                    COALESCE(o."Полное наименование", 'Не указано') AS "Полное название", 
                    COALESCE(o."Краткое наименование", 'Не указано') AS "Краткое название", 
                    'Исходящий' AS "Тип документа"
                FROM db."Исходящий документ" d
                LEFT JOIN db."Организация" o ON d."Направлен_организация" = o.id
                LEFT JOIN db."Лицо" л ON d."Направлен" = л.id
                LEFT JOIN db."users" u ON d."user_id" = u.id
            ''')

            results = cursor.fetchall()

            if results:
                st.write("Результаты запроса:")

                # Обработка результатов
                processed_results = []
                for row in results:
                    print(row)

                    date, number, fio, name, inn, full_name, short_name, doc_type = row

                    fio = fio if fio != 'Мнимый Мнимый Мнимый' else '==========================>'
                    inn = inn if inn and inn != '0' else '<Не указано>'
                    full_name = full_name if full_name and full_name != 'Мнимый' else '<Не указано>'
                    short_name = short_name if short_name and short_name != 'Мнимый' else '<Не указано>'

                    # Добавляем строку в обработанные результаты
                    processed_results.append((date, number, fio, name, inn, full_name, short_name, doc_type))

                # Создание DataFrame
                df = pd.DataFrame(
                    processed_results,
                    columns=["Дата", "Номер", "ФИО", "Имя Пользователя", "ИНН", "Полное наименование", "Краткое название", "Тип документа"]
                )
                df.reset_index(drop=True, inplace=True)

                # Отображение таблицы
                st.dataframe(df.style.hide(axis="index"))
            else:
                st.write("Нет данных для указанного пользователя.")
    except Exception as e:
        st.error("Произошла ошибка при выполнении запроса.")
        print(f"Error occurred: {e}")

    if (st.button("Назад")):
        st.session_state["current_page"] = "come_mess"
        st.session_state["rerun"] = True

def come_mess():
    st.title("Выбор типа документа")
    if st.button("Добавить документ"):
        st.session_state["current_page"] = "add_doc"
        st.session_state["rerun"] = True

    if st.button("Исходящий документ"):
        st.session_state["current_page"] = 'ischod'
        st.session_state["rerun"] = True

    if st.button("Входящий документ"):
        st.session_state["current_page"] = 'vhod'
        st.session_state["rerun"] = True

    if st.button("Посмотреть все"):
        st.session_state["current_page"] = 'vse_pol'
        st.session_state["rerun"] = True

    # Проверяем уровень пользователя
    user_level = st.session_state.get("user_level", 1)

    if user_level == '2':
        if st.button("Посмотреть все документы пользователей"):
            st.session_state["current_page"] = 'vse_pol_admin'
            st.session_state["rerun"] = True

def main():
    # Проверяем текущее состояние страницы
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "login"  # Стартовая страница
        st.session_state["rerun"] = False  # Инициализируем скрытый триггер

    # Отображаем соответствующую страницу
    if st.session_state["current_page"] == "login":
        login()
    elif st.session_state["current_page"] == "registration":
        registration()
    elif st.session_state["current_page"] == "come_mess":
        come_mess()
    elif st.session_state["current_page"] == "add_doc":
        add_doc()
    elif st.session_state["current_page"] == "phys_or_org":
        phys_or_org()
    elif st.session_state["current_page"] == "add_vhod_doc":
        add_vhod_doc()
    elif st.session_state["current_page"] == "add_vhod_doc_org":
        add_vhod_doc_org()
    elif st.session_state["current_page"] == "send_doc":
        send_doc()
    elif st.session_state["current_page"] == "add_lic":
        add_lic()
    elif st.session_state["current_page"] == "add_org":
        add_org()
    elif st.session_state["current_page"] == "ischod":
        ischod()
    elif st.session_state["current_page"] == "vhod":
        vhod()
    elif st.session_state["current_page"] == "vse_pol":
        vse_pol()
    elif st.session_state["current_page"] == "vse_pol_admin":
        vse_pol_admin()

    # Принудительная перерисовка
    if st.session_state["rerun"]:
        st.session_state["rerun"] = False  # Сбрасываем триггер
        st.rerun()

if __name__ == "__main__":
    main()
