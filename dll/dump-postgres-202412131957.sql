--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

-- Started on 2024-12-13 19:57:49

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY db."Исходящий документ" DROP CONSTRAINT "Исходящий документ_user_id_fkey";
ALTER TABLE ONLY db."Входящий документ" DROP CONSTRAINT "Входящий документ_user_id_fkey";
ALTER TABLE ONLY db."Входящий документ" DROP CONSTRAINT "fk_получен_от_организация";
ALTER TABLE ONLY db."Входящий документ" DROP CONSTRAINT "fk_получен_от";
ALTER TABLE ONLY db."Исходящий документ" DROP CONSTRAINT "fk_направлен_от";
ALTER TABLE ONLY db."Исходящий документ" DROP CONSTRAINT "fk_Направлен_от_организация";
ALTER TABLE ONLY db."Адрес" DROP CONSTRAINT fk_id_usersss;
ALTER TABLE ONLY db."Адрес" DROP CONSTRAINT fk_id_users;
ALTER TABLE ONLY db."Организация" DROP CONSTRAINT fk_id_users;
ALTER TABLE ONLY db."Должность" DROP CONSTRAINT fk_id_users;
ALTER TABLE ONLY db."Почта" DROP CONSTRAINT fk_id_users;
ALTER TABLE ONLY db."Телефон" DROP CONSTRAINT fk_id_users;
DROP TRIGGER move_post_trigger ON db."Лицо";
DROP TRIGGER move_phone_trigger ON db."Лицо";
DROP TRIGGER move_email_trigger ON db."Лицо";
ALTER TABLE ONLY db."Телефон" DROP CONSTRAINT "Телефон_pkey";
ALTER TABLE ONLY db."Почта" DROP CONSTRAINT "Почта_pkey";
ALTER TABLE ONLY db."Организация" DROP CONSTRAINT "Организация_pkey";
ALTER TABLE ONLY db."Лицо" DROP CONSTRAINT "Лицо_pkey";
ALTER TABLE ONLY db."Исходящий документ" DROP CONSTRAINT "Исходящий документ_Номер_unique";
ALTER TABLE ONLY db."Исходящий документ" DROP CONSTRAINT "Исходящий документ_pkey";
ALTER TABLE ONLY db."Должность" DROP CONSTRAINT "Должность_pkey";
ALTER TABLE ONLY db."Входящий документ" DROP CONSTRAINT "Входящий документ_Номер_unique";
ALTER TABLE ONLY db."Входящий документ" DROP CONSTRAINT "Входящий документ_pkey";
ALTER TABLE ONLY db."Адрес" DROP CONSTRAINT "Адрес_pkey";
ALTER TABLE ONLY db.users DROP CONSTRAINT users_username_key;
ALTER TABLE ONLY db.users DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY db.users DROP CONSTRAINT users_email_key;
ALTER TABLE ONLY db.users DROP CONSTRAINT unique_username;
ALTER TABLE ONLY db.users DROP CONSTRAINT unique_email;
ALTER TABLE ONLY db."Организация" DROP CONSTRAINT unique_address;
ALTER TABLE db."Адрес" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE db.users ALTER COLUMN id DROP DEFAULT;
DROP TABLE db."Телефон";
DROP TABLE db."Почта";
DROP TABLE db."Организация";
DROP TABLE db."Лицо";
DROP TABLE db."Исходящий документ";
DROP TABLE db."Должность";
DROP TABLE db."Входящий документ";
DROP SEQUENCE db."Адрес_id_seq";
DROP TABLE db."Адрес";
DROP SEQUENCE db.users_id_seq;
DROP TABLE db.users;
DROP SCHEMA db;
--
-- TOC entry 12 (class 2615 OID 32960)
-- Name: db; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA db;


ALTER SCHEMA db OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 250 (class 1259 OID 57522)
-- Name: users; Type: TABLE; Schema: db; Owner: postgres
--

CREATE TABLE db.users (
    id bigint NOT NULL,
    username text NOT NULL,
    password_hash text NOT NULL,
    email text,
    full_name text,
    created_at timestamp without time zone DEFAULT now(),
    level character varying(10) DEFAULT 'user'::character varying NOT NULL
);


ALTER TABLE db.users OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 57521)
-- Name: users_id_seq; Type: SEQUENCE; Schema: db; Owner: postgres
--

CREATE SEQUENCE db.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE db.users_id_seq OWNER TO postgres;

--
-- TOC entry 4998 (class 0 OID 0)
-- Dependencies: 249
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: db; Owner: postgres
--

ALTER SEQUENCE db.users_id_seq OWNED BY db.users.id;


--
-- TOC entry 252 (class 1259 OID 57598)
-- Name: Адрес; Type: TABLE; Schema: db; Owner: postgres
--

CREATE TABLE db."Адрес" (
    id bigint NOT NULL,
    "страна" text,
    "регион" text,
    "индекс" integer,
    "район" text,
    "населенный_пункт" text,
    "улица" text,
    "дом" text,
    "корпус" text,
    "строение" text,
    org_id bigint
);


ALTER TABLE db."Адрес" OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 57597)
-- Name: Адрес_id_seq; Type: SEQUENCE; Schema: db; Owner: postgres
--

CREATE SEQUENCE db."Адрес_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE db."Адрес_id_seq" OWNER TO postgres;

--
-- TOC entry 4999 (class 0 OID 0)
-- Dependencies: 251
-- Name: Адрес_id_seq; Type: SEQUENCE OWNED BY; Schema: db; Owner: postgres
--

ALTER SEQUENCE db."Адрес_id_seq" OWNED BY db."Адрес".id;


--
-- TOC entry 247 (class 1259 OID 33003)
-- Name: Входящий документ; Type: TABLE; Schema: db; Owner: postgres
--

CREATE TABLE db."Входящий документ" (
    id bigint NOT NULL,
    "Дата" date NOT NULL,
    "Номер" text NOT NULL,
    "Получен от" bigint,
    user_id bigint,
    "Получен_от_организация" bigint
);


ALTER TABLE db."Входящий документ" OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 32968)
-- Name: Должность; Type: TABLE; Schema: db; Owner: postgres
--

CREATE TABLE db."Должность" (
    id bigint NOT NULL,
    "Название" text NOT NULL,
    "Дата_вступления" date NOT NULL,
    user_id bigint
);


ALTER TABLE db."Должность" OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 33010)
-- Name: Исходящий документ; Type: TABLE; Schema: db; Owner: postgres
--

CREATE TABLE db."Исходящий документ" (
    id bigint NOT NULL,
    "Дата" date NOT NULL,
    "Номер" text NOT NULL,
    "Направлен" bigint NOT NULL,
    user_id bigint,
    "Направлен_организация" bigint
);


ALTER TABLE db."Исходящий документ" OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 32996)
-- Name: Лицо; Type: TABLE; Schema: db; Owner: postgres
--

CREATE TABLE db."Лицо" (
    id bigint NOT NULL,
    "Фамилия" text NOT NULL,
    "Имя" text NOT NULL,
    "Отчество" text NOT NULL,
    "Телефон" text NOT NULL,
    "e-mail" text NOT NULL,
    "Должность" text,
    "Работает в" text NOT NULL,
    "Дата_вступления" date
);


ALTER TABLE db."Лицо" OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 32989)
-- Name: Организация; Type: TABLE; Schema: db; Owner: postgres
--

CREATE TABLE db."Организация" (
    id bigint NOT NULL,
    "Полное наименование" text NOT NULL,
    "Краткое наименование" text NOT NULL,
    "ОГРН" bigint NOT NULL,
    "ИНН" bigint NOT NULL,
    "Адрес юридический" bigint NOT NULL,
    "Адрес фактический" bigint NOT NULL,
    "Адрес почтовый" bigint NOT NULL,
    "Телефон" text NOT NULL,
    "e-mail" text NOT NULL,
    "Руководитель" bigint
);


ALTER TABLE db."Организация" OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 32982)
-- Name: Почта; Type: TABLE; Schema: db; Owner: postgres
--

CREATE TABLE db."Почта" (
    id bigint NOT NULL,
    "e-mail" text NOT NULL,
    user_id bigint
);


ALTER TABLE db."Почта" OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 32975)
-- Name: Телефон; Type: TABLE; Schema: db; Owner: postgres
--

CREATE TABLE db."Телефон" (
    id bigint NOT NULL,
    "Номер" text NOT NULL,
    id_users bigint
);


ALTER TABLE db."Телефон" OWNER TO postgres;

--
-- TOC entry 4786 (class 2604 OID 57525)
-- Name: users id; Type: DEFAULT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db.users ALTER COLUMN id SET DEFAULT nextval('db.users_id_seq'::regclass);


--
-- TOC entry 4789 (class 2604 OID 57695)
-- Name: Адрес id; Type: DEFAULT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Адрес" ALTER COLUMN id SET DEFAULT nextval('db."Адрес_id_seq"'::regclass);


--
-- TOC entry 4990 (class 0 OID 57522)
-- Dependencies: 250
-- Data for Name: users; Type: TABLE DATA; Schema: db; Owner: postgres
--

INSERT INTO db.users VALUES (4, 'vasyan', 'af2c5583bd71476385bf5371fd406a8655d2ee043b7c80a0f0a00bc26be89653', 'efeded@odbc.com', 'asvuasvcu', '2024-12-05 17:40:41.775544', '1');
INSERT INTO db.users VALUES (5, 'OUTWEST', 'aa192f7c071474b15a2e2ea3309d269359b31442d2562c81e4f2f4878175bd37', 'fedoresm@icloud.com', 'Эсмедляев Федор Романович', '2024-12-05 17:41:37.454393', '2');
INSERT INTO db.users VALUES (6, 'slark221', 'a1491c54170c7da7c83ad474741f1db444c9d18f73181c5a321d9951608427af', 'ko3@front.ru', 'Головенко Анатолий Валерьевич', '2024-12-07 21:02:53.76956', '1');
INSERT INTO db.users VALUES (7, 'new', '7fb26a8732f70c7392214b9056c2cd60f5b2d8a6e64d2356ae396297fd750b4a', 'asoubasd', 'dl;jbidc', '2024-12-10 19:05:44.72452', '1');
INSERT INTO db.users VALUES (8, 'fedos_test_nout', '28d0537a45f037bf750ab53aabea52ed9f970aa74839cc9fc3ef0d98edcbc61f', 'ko1@front.ru', 'Евгений Два Три', '2024-12-11 18:01:05.361016', '1');


--
-- TOC entry 4992 (class 0 OID 57598)
-- Dependencies: 252
-- Data for Name: Адрес; Type: TABLE DATA; Schema: db; Owner: postgres
--

INSERT INTO db."Адрес" VALUES (1, 'Россия', 'г.Москва', 131232, 'Кунцево', 'вссввс', 'тверская', '1', '1', '2', 8);
INSERT INTO db."Адрес" VALUES (3, '123', 'г.Москва', 1211221, NULL, NULL, NULL, NULL, NULL, NULL, 8);


--
-- TOC entry 4987 (class 0 OID 33003)
-- Dependencies: 247
-- Data for Name: Входящий документ; Type: TABLE DATA; Schema: db; Owner: postgres
--

INSERT INTO db."Входящий документ" VALUES (10, '1111-11-11', '123123123', 0, 4, 1);
INSERT INTO db."Входящий документ" VALUES (13, '1111-11-11', '65656666', 0, 6, NULL);
INSERT INTO db."Входящий документ" VALUES (14, '2026-12-12', '565665655656', 0, 4, NULL);
INSERT INTO db."Входящий документ" VALUES (11, '1222-11-11', '12121212', 2, 4, NULL);
INSERT INTO db."Входящий документ" VALUES (12, '2112-12-12', '89898989898', 4, 6, NULL);
INSERT INTO db."Входящий документ" VALUES (15, '2024-12-10', '8778788778788787', 8, 5, NULL);
INSERT INTO db."Входящий документ" VALUES (16, '2000-12-12', '9219233232132', 9, 7, NULL);
INSERT INTO db."Входящий документ" VALUES (17, '2020-04-05', '23321312312312132', 10, 7, NULL);
INSERT INTO db."Входящий документ" VALUES (18, '2017-12-12', '123213213132313213123123', 11, 7, NULL);


--
-- TOC entry 4982 (class 0 OID 32968)
-- Dependencies: 242
-- Data for Name: Должность; Type: TABLE DATA; Schema: db; Owner: postgres
--

INSERT INTO db."Должность" VALUES (1, 'Генеральный директор', '2020-01-01', NULL);
INSERT INTO db."Должность" VALUES (2, 'Менеджер', '2021-06-15', NULL);
INSERT INTO db."Должность" VALUES (3, 'Бухгалтер', '2019-03-10', NULL);
INSERT INTO db."Должность" VALUES (4, 'секретарь', '2013-12-12', 8);


--
-- TOC entry 4988 (class 0 OID 33010)
-- Dependencies: 248
-- Data for Name: Исходящий документ; Type: TABLE DATA; Schema: db; Owner: postgres
--

INSERT INTO db."Исходящий документ" VALUES (1, '2023-11-02', 'OUT-001', 1, NULL, NULL);
INSERT INTO db."Исходящий документ" VALUES (3, '2024-12-07', '123123123', 0, 5, 1);
INSERT INTO db."Исходящий документ" VALUES (9, '1999-07-07', '878787', 0, 4, 8);
INSERT INTO db."Исходящий документ" VALUES (2, '2024-12-07', '23123123', 0, 5, NULL);
INSERT INTO db."Исходящий документ" VALUES (4, '1111-12-12', '123123', 0, 5, NULL);
INSERT INTO db."Исходящий документ" VALUES (5, '8888-12-12', '777777', 0, 5, NULL);
INSERT INTO db."Исходящий документ" VALUES (6, '2024-12-08', '09809098', 2, 5, NULL);
INSERT INTO db."Исходящий документ" VALUES (7, '2024-12-09', '7867654567', 5, 4, NULL);
INSERT INTO db."Исходящий документ" VALUES (10, '2024-12-10', '1231231231231', 0, 5, 9);
INSERT INTO db."Исходящий документ" VALUES (11, '2024-12-13', '56757678678678', 0, 5, 10);


--
-- TOC entry 4986 (class 0 OID 32996)
-- Dependencies: 246
-- Data for Name: Лицо; Type: TABLE DATA; Schema: db; Owner: postgres
--

INSERT INTO db."Лицо" VALUES (1, 'Иванов', 'Иван', 'Иванович', '1', '1', '1', '1', NULL);
INSERT INTO db."Лицо" VALUES (2, 'Эсмедляев', 'Федор', 'Романович', 'Null', 'Null', '0', '0', NULL);
INSERT INTO db."Лицо" VALUES (3, 'Полыга', 'Руслан', 'Борисыч', 'Null', 'Null', '0', '0', NULL);
INSERT INTO db."Лицо" VALUES (0, 'Мнимый', 'Мнимый', 'Мнимый', 'Мнимый', 'Мнимый', '0', '0', NULL);
INSERT INTO db."Лицо" VALUES (4, 'Епифанов', 'Евгений', 'Евгеньевич', 'Null', 'Null', '0', '0', NULL);
INSERT INTO db."Лицо" VALUES (5, 'Иванов', 'Антон', 'Русланович', 'Null', 'Null', '0', '0', NULL);
INSERT INTO db."Лицо" VALUES (6, 'Иванов', 'Иван', 'Иванович', '+1234567890', 'ivanov@example.com', '3', '1', NULL);
INSERT INTO db."Лицо" VALUES (7, 'Иванов', 'Иван', 'Иванович', '+1234567890', 'ivanov@example.com', '3', '1', NULL);
INSERT INTO db."Лицо" VALUES (9, 'Сергеев', 'Максим', 'Александрович', '21387987123987', 'Null', '0', '0', '1970-01-01');
INSERT INTO db."Лицо" VALUES (10, 'Антонов', 'Сергей', 'Валерьевич', 'Null', 'Null', '0', '0', '1970-01-01');
INSERT INTO db."Лицо" VALUES (11, 'Рофлан', 'тест', 'один', 'Null', 'Null', '0', '0', '1970-01-01');
INSERT INTO db."Лицо" VALUES (8, 'Салихов', 'Тимур', 'Русланович', '+8(903)671-12-23', 'novaya@gmail.com', 'секретарь', 'fghbgh', '2013-12-12');


--
-- TOC entry 4985 (class 0 OID 32989)
-- Dependencies: 245
-- Data for Name: Организация; Type: TABLE DATA; Schema: db; Owner: postgres
--

INSERT INTO db."Организация" VALUES (1, 'ООО Рога и Копыта', 'Рога и Копыта', 7986987697, 9876543210, 1, 2, 3, '+7 (495) 987-65-43', 'info@company.ru', 2);
INSERT INTO db."Организация" VALUES (8, '', '"СЛарк"', 1231233, 0, 3, 1, 1, '+8(999)9923213', 'lox@negr.com', 2);
INSERT INTO db."Организация" VALUES (9, '', '"Тестер"', 1, 0, 4, 1, 1, 'Null', 'Null', 0);
INSERT INTO db."Организация" VALUES (10, 'ООО МАИ', '', 1, 0, 5, 1, 1, 'Null', 'Null', 0);


--
-- TOC entry 4984 (class 0 OID 32982)
-- Dependencies: 244
-- Data for Name: Почта; Type: TABLE DATA; Schema: db; Owner: postgres
--

INSERT INTO db."Почта" VALUES (1, 'director@example.com', NULL);
INSERT INTO db."Почта" VALUES (2, 'manager@example.com', NULL);
INSERT INTO db."Почта" VALUES (3, 'accountant@example.com', NULL);
INSERT INTO db."Почта" VALUES (4, 'novaya@gmail.com', 8);
INSERT INTO db."Почта" VALUES (5, 'Null', 9);
INSERT INTO db."Почта" VALUES (6, 'Null', 10);
INSERT INTO db."Почта" VALUES (7, 'Null', 11);


--
-- TOC entry 4983 (class 0 OID 32975)
-- Dependencies: 243
-- Data for Name: Телефон; Type: TABLE DATA; Schema: db; Owner: postgres
--

INSERT INTO db."Телефон" VALUES (1, '+7 (495) 123-45-67', NULL);
INSERT INTO db."Телефон" VALUES (2, '+7 (916) 234-56-78', NULL);
INSERT INTO db."Телефон" VALUES (3, '+7 (812) 345-67-89', NULL);
INSERT INTO db."Телефон" VALUES (4, '+1234567890', 6);
INSERT INTO db."Телефон" VALUES (5, '+1234567890', 7);
INSERT INTO db."Телефон" VALUES (10, '+8(903)671-12-23', 8);
INSERT INTO db."Телефон" VALUES (12, '21387987123987', 9);
INSERT INTO db."Телефон" VALUES (13, 'Null', 10);
INSERT INTO db."Телефон" VALUES (14, 'Null', 11);


--
-- TOC entry 5000 (class 0 OID 0)
-- Dependencies: 249
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: db; Owner: postgres
--

SELECT pg_catalog.setval('db.users_id_seq', 1, false);


--
-- TOC entry 5001 (class 0 OID 0)
-- Dependencies: 251
-- Name: Адрес_id_seq; Type: SEQUENCE SET; Schema: db; Owner: postgres
--

SELECT pg_catalog.setval('db."Адрес_id_seq"', 1, false);


--
-- TOC entry 4797 (class 2606 OID 57714)
-- Name: Организация unique_address; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Организация"
    ADD CONSTRAINT unique_address UNIQUE ("Адрес юридический");


--
-- TOC entry 4811 (class 2606 OID 57548)
-- Name: users unique_email; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db.users
    ADD CONSTRAINT unique_email UNIQUE (email);


--
-- TOC entry 4813 (class 2606 OID 57546)
-- Name: users unique_username; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db.users
    ADD CONSTRAINT unique_username UNIQUE (username);


--
-- TOC entry 4815 (class 2606 OID 57534)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 4817 (class 2606 OID 57530)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4819 (class 2606 OID 57532)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4821 (class 2606 OID 57697)
-- Name: Адрес Адрес_pkey; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Адрес"
    ADD CONSTRAINT "Адрес_pkey" PRIMARY KEY (id);


--
-- TOC entry 4803 (class 2606 OID 33009)
-- Name: Входящий документ Входящий документ_pkey; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Входящий документ"
    ADD CONSTRAINT "Входящий документ_pkey" PRIMARY KEY (id);


--
-- TOC entry 4805 (class 2606 OID 33053)
-- Name: Входящий документ Входящий документ_Номер_unique; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Входящий документ"
    ADD CONSTRAINT "Входящий документ_Номер_unique" UNIQUE ("Номер");


--
-- TOC entry 4791 (class 2606 OID 32974)
-- Name: Должность Должность_pkey; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Должность"
    ADD CONSTRAINT "Должность_pkey" PRIMARY KEY (id);


--
-- TOC entry 4807 (class 2606 OID 33016)
-- Name: Исходящий документ Исходящий документ_pkey; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Исходящий документ"
    ADD CONSTRAINT "Исходящий документ_pkey" PRIMARY KEY (id);


--
-- TOC entry 4809 (class 2606 OID 33055)
-- Name: Исходящий документ Исходящий документ_Номер_unique; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Исходящий документ"
    ADD CONSTRAINT "Исходящий документ_Номер_unique" UNIQUE ("Номер");


--
-- TOC entry 4801 (class 2606 OID 33002)
-- Name: Лицо Лицо_pkey; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Лицо"
    ADD CONSTRAINT "Лицо_pkey" PRIMARY KEY (id);


--
-- TOC entry 4799 (class 2606 OID 32995)
-- Name: Организация Организация_pkey; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Организация"
    ADD CONSTRAINT "Организация_pkey" PRIMARY KEY (id);


--
-- TOC entry 4795 (class 2606 OID 57661)
-- Name: Почта Почта_pkey; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Почта"
    ADD CONSTRAINT "Почта_pkey" PRIMARY KEY (id);


--
-- TOC entry 4793 (class 2606 OID 57631)
-- Name: Телефон Телефон_pkey; Type: CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Телефон"
    ADD CONSTRAINT "Телефон_pkey" PRIMARY KEY (id);


--
-- TOC entry 4834 (class 2620 OID 57663)
-- Name: Лицо move_email_trigger; Type: TRIGGER; Schema: db; Owner: postgres
--

CREATE TRIGGER move_email_trigger AFTER INSERT OR UPDATE ON db."Лицо" FOR EACH ROW EXECUTE FUNCTION public.move_email_to_table();


--
-- TOC entry 4835 (class 2620 OID 57650)
-- Name: Лицо move_phone_trigger; Type: TRIGGER; Schema: db; Owner: postgres
--

CREATE TRIGGER move_phone_trigger AFTER INSERT OR UPDATE ON db."Лицо" FOR EACH ROW EXECUTE FUNCTION public.move_phone_to_table();


--
-- TOC entry 4836 (class 2620 OID 57677)
-- Name: Лицо move_post_trigger; Type: TRIGGER; Schema: db; Owner: postgres
--

CREATE TRIGGER move_post_trigger AFTER INSERT OR UPDATE ON db."Лицо" FOR EACH ROW EXECUTE FUNCTION public.move_post_to_table();


--
-- TOC entry 4823 (class 2606 OID 57633)
-- Name: Телефон fk_id_users; Type: FK CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Телефон"
    ADD CONSTRAINT fk_id_users FOREIGN KEY (id_users) REFERENCES db."Лицо"(id) ON DELETE CASCADE;


--
-- TOC entry 4824 (class 2606 OID 57664)
-- Name: Почта fk_id_users; Type: FK CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Почта"
    ADD CONSTRAINT fk_id_users FOREIGN KEY (user_id) REFERENCES db."Лицо"(id) ON DELETE CASCADE;


--
-- TOC entry 4822 (class 2606 OID 57678)
-- Name: Должность fk_id_users; Type: FK CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Должность"
    ADD CONSTRAINT fk_id_users FOREIGN KEY (user_id) REFERENCES db."Лицо"(id) ON DELETE CASCADE;


--
-- TOC entry 4825 (class 2606 OID 57698)
-- Name: Организация fk_id_users; Type: FK CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Организация"
    ADD CONSTRAINT fk_id_users FOREIGN KEY ("Руководитель") REFERENCES db."Лицо"(id) ON DELETE CASCADE;


--
-- TOC entry 4832 (class 2606 OID 57720)
-- Name: Адрес fk_id_users; Type: FK CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Адрес"
    ADD CONSTRAINT fk_id_users FOREIGN KEY (id) REFERENCES db."Организация"("Адрес юридический") ON DELETE CASCADE;


--
-- TOC entry 4833 (class 2606 OID 57708)
-- Name: Адрес fk_id_usersss; Type: FK CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Адрес"
    ADD CONSTRAINT fk_id_usersss FOREIGN KEY (org_id) REFERENCES db."Организация"(id) ON DELETE CASCADE;


--
-- TOC entry 4829 (class 2606 OID 57583)
-- Name: Исходящий документ fk_Направлен_от_организация; Type: FK CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Исходящий документ"
    ADD CONSTRAINT "fk_Направлен_от_организация" FOREIGN KEY ("Направлен_организация") REFERENCES db."Организация"(id) ON DELETE SET NULL;


--
-- TOC entry 4830 (class 2606 OID 57588)
-- Name: Исходящий документ fk_направлен_от; Type: FK CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Исходящий документ"
    ADD CONSTRAINT "fk_направлен_от" FOREIGN KEY ("Направлен") REFERENCES db."Лицо"(id) ON DELETE SET NULL;


--
-- TOC entry 4826 (class 2606 OID 57561)
-- Name: Входящий документ fk_получен_от; Type: FK CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Входящий документ"
    ADD CONSTRAINT "fk_получен_от" FOREIGN KEY ("Получен от") REFERENCES db."Лицо"(id) ON DELETE SET NULL;


--
-- TOC entry 4827 (class 2606 OID 57571)
-- Name: Входящий документ fk_получен_от_организация; Type: FK CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Входящий документ"
    ADD CONSTRAINT "fk_получен_от_организация" FOREIGN KEY ("Получен_от_организация") REFERENCES db."Организация"(id) ON DELETE SET NULL;


--
-- TOC entry 4828 (class 2606 OID 57535)
-- Name: Входящий документ Входящий документ_user_id_fkey; Type: FK CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Входящий документ"
    ADD CONSTRAINT "Входящий документ_user_id_fkey" FOREIGN KEY (user_id) REFERENCES db.users(id);


--
-- TOC entry 4831 (class 2606 OID 57540)
-- Name: Исходящий документ Исходящий документ_user_id_fkey; Type: FK CONSTRAINT; Schema: db; Owner: postgres
--

ALTER TABLE ONLY db."Исходящий документ"
    ADD CONSTRAINT "Исходящий документ_user_id_fkey" FOREIGN KEY (user_id) REFERENCES db.users(id);


-- Completed on 2024-12-13 19:57:49

--
-- PostgreSQL database dump complete
--

