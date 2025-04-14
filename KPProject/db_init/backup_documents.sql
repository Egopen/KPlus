--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-04-14 15:52:17

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 24603)
-- Name: document_contents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.document_contents (
    id integer NOT NULL,
    content text NOT NULL,
    document_id integer NOT NULL
);


ALTER TABLE public.document_contents OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24602)
-- Name: document_contents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.document_contents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.document_contents_id_seq OWNER TO postgres;

--
-- TOC entry 4928 (class 0 OID 0)
-- Dependencies: 219
-- Name: document_contents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.document_contents_id_seq OWNED BY public.document_contents.id;


--
-- TOC entry 218 (class 1259 OID 24594)
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents (
    id integer NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    doc_type character varying(255) NOT NULL,
    title character varying(255) NOT NULL
);


ALTER TABLE public.documents OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 24593)
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.documents_id_seq OWNER TO postgres;

--
-- TOC entry 4929 (class 0 OID 0)
-- Dependencies: 217
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;


--
-- TOC entry 222 (class 1259 OID 24619)
-- Name: statistics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.statistics (
    id integer NOT NULL,
    visited_count integer DEFAULT 0 NOT NULL,
    avr_time integer NOT NULL,
    document_id integer NOT NULL
);


ALTER TABLE public.statistics OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24618)
-- Name: statistics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.statistics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.statistics_id_seq OWNER TO postgres;

--
-- TOC entry 4930 (class 0 OID 0)
-- Dependencies: 221
-- Name: statistics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.statistics_id_seq OWNED BY public.statistics.id;


--
-- TOC entry 4755 (class 2604 OID 24606)
-- Name: document_contents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_contents ALTER COLUMN id SET DEFAULT nextval('public.document_contents_id_seq'::regclass);


--
-- TOC entry 4752 (class 2604 OID 24597)
-- Name: documents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);


--
-- TOC entry 4756 (class 2604 OID 24622)
-- Name: statistics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statistics ALTER COLUMN id SET DEFAULT nextval('public.statistics_id_seq'::regclass);


--
-- TOC entry 4920 (class 0 OID 24603)
-- Dependencies: 220
-- Data for Name: document_contents; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.document_contents (id, content, document_id) VALUES (1, '<div><h1>Отсутствие гарантий исключительности права использования франшизы</h1><div><strong>Описание:</strong> Правообладатель может предоставлять аналогичные права другим лицам на той же территории. (п. 2 ст. 1033 ГК РФ)</div><div><strong>Уровень риска:</strong> Высокий</div></div>', 1);
INSERT INTO public.document_contents (id, content, document_id) VALUES (2, '<div><h1>Ограничения на ведение самостоятельной деятельности</h1><div><strong>Описание:</strong> Такой запрет может сильно ограничить мобильность бизнеса и открытие аналогичных точек. (п. 1 ст. 1033 ГК РФ)</div><div><strong>Уровень риска:</strong> Очень высокий</div></div>', 2);
INSERT INTO public.document_contents (id, content, document_id) VALUES (3, '<div><h1>Штрафные санкции за односторонний отказ от договора</h1><div><strong>Описание:</strong> Франчайзи обязан выплачивать значительную компенсацию при досрочном расторжении. Зачастую большие затраты. (ст. 1037 ГК РФ)</div><div><strong>Уровень риска:</strong> Повышенный</div></div>', 3);
INSERT INTO public.document_contents (id, content, document_id) VALUES (4, '<div><h1>Обязанность соблюдать стандарты бизнес-процессов без возможности адаптации под локальный рынок</h1><div><strong>Описание:</strong> Франчайзи не может изменять технологию, ассортимент или методы работы даже при их неэффективности. Учитывайте особенности местного рынка. (ст. 1032 ГК РФ)</div><div><strong>Уровень риска:</strong> Умеренный</div></div>', 4);
INSERT INTO public.document_contents (id, content, document_id) VALUES (5, '<div><h1>Отсутствие четких критериев качества товаров/услуг</h1><div><strong>Описание:</strong> Франчайзор может отказаться от приемки работ/товаров под предлогом "несоответствия стандартам". (п. 2 ст. 1032 ГК РФ)</div><div><strong>Уровень риска:</strong> Очень высокий</div></div>', 5);
INSERT INTO public.document_contents (id, content, document_id) VALUES (6, '<div><h1>Запрет на оспаривание исключительных прав франчайзора</h1><div><strong>Описание:</strong> Пользователь не может оспорить товарный знак или технологию, даже если они нарушают чьи-то права. (п. 2 ст. 1038 ГК РФ)</div><div><strong>Уровень риска:</strong> Высокий</div></div>', 6);
INSERT INTO public.document_contents (id, content, document_id) VALUES (7, '<div><h1>Одностороннее изменение франчайзором условий договора</h1><div><strong>Описание:</strong> Включение условия о возможности изменения ключевых параметров договора без согласия франчайзи.</div><div><strong>Уровень риска:</strong> Очень высокий</div></div>', 7);
INSERT INTO public.document_contents (id, content, document_id) VALUES (8, '<div><h1>Ограничение ответственности франчайзора за недобросовестные действия</h1><div><strong>Описание:</strong> Исключение или минимизация ответственности за недостоверную информацию о франшизе. (ст. 1034 ГК РФ)</div><div><strong>Уровень риска:</strong> Очень высокий</div></div>', 8);
INSERT INTO public.document_contents (id, content, document_id) VALUES (9, '<div><h1>Запрет на оспаривание товарного знака или технологии франчайзора</h1><div><strong>Описание:</strong> Франчайзи не может оспаривать товарный знак или технологию, даже если они нарушают чьи-то права. (п. 2 ст. 1038 ГК РФ)</div><div><strong>Уровень риска:</strong> Высокий</div></div>', 9);
INSERT INTO public.document_contents (id, content, document_id) VALUES (10, '<div><h1>Запрет на самостоятельное изменение ценообразования</h1><div><strong>Описание:</strong> Франчайзор диктует фиксированные цены, не учитывающие локальную экономическую ситуацию. (ст. 1033 ГК РФ)</div><div><strong>Уровень риска:</strong> Повышенный</div></div>', 10);
INSERT INTO public.document_contents (id, content, document_id) VALUES (11, '<div><h1>Обязанность закупать товары/сырье только у франчайзора или его партнеров по завышенным ценам</h1><div><strong>Описание:</strong> Создает зависимость и снижает рентабельность. (п. 1 ст. 1033 ГК РФ)</div><div><strong>Уровень риска:</strong> Очень высокий</div></div>', 11);
INSERT INTO public.document_contents (id, content, document_id) VALUES (12, '<div><h1>Автоматическое продление договора без согласия франчайзи</h1><div><strong>Описание:</strong> Таким образом происходит "молчаливое согласие" на продление с повышением платежей.</div><div><strong>Уровень риска:</strong> Высокий</div></div>', 12);
INSERT INTO public.document_contents (id, content, document_id) VALUES (13, '<div><h1>Штрафы за невыполнение плановых показателей</h1><div><strong>Описание:</strong> Даже если показатели нереалистичны для региона.</div><div><strong>Уровень риска:</strong> Очень высокий</div></div>', 13);
INSERT INTO public.document_contents (id, content, document_id) VALUES (14, '<div><h1>Отсутствие четкого порядка разрешения споров</h1><div><strong>Описание:</strong> Все споры рассматриваются в суде по месту нахождения франчайзора. (ст. 1038 ГК РФ)</div><div><strong>Уровень риска:</strong> Высокий</div></div>', 14);
INSERT INTO public.document_contents (id, content, document_id) VALUES (15, '<div><h1>Запрет на ведение аналогичного бизнеса после прекращения договора</h1><div><strong>Описание:</strong> Блокирует развитие независимого бренда после прекращения договора. (п. 2 ст. 1037 ГК РФ)</div><div><strong>Уровень риска:</strong> Очень высокий</div></div>', 15);
INSERT INTO public.document_contents (id, content, document_id) VALUES (16, '<div><h1>Непропорциональное распределение рекламных расходов</h1><div><strong>Описание:</strong> Франчайзи обязан финансировать рекламу без учета локальной эффективности. Высокие затраты. (ст. 1034 ГК РФ)</div><div><strong>Уровень риска:</strong> Высокий</div></div>', 16);
INSERT INTO public.document_contents (id, content, document_id) VALUES (17, '<div><h1>Отсутствие компенсации за улучшения, внесенные франчайзи</h1><div><strong>Описание:</strong> Все модификации бизнес-модели могут быть недопустимы по договору, иногда же передаваться правообладателю, что приводит к высоким затратам. (ст. 1039 ГК РФ)</div><div><strong>Уровень риска:</strong> Повышенный</div></div>', 17);
INSERT INTO public.document_contents (id, content, document_id) VALUES (18, '<div><h1>Аудит деятельности франчайзи</h1><div><strong>Описание:</strong> Франчайзор вправе проводить проверки с возможностью взыскания штрафов за "нарушения". Обязательно проверяйте дополнительные соглашения и документацию, регулирующую проведение аудита. (ст. 1032 ГК РФ)</div><div><strong>Уровень риска:</strong> Умеренный</div></div>', 18);
INSERT INTO public.document_contents (id, content, document_id) VALUES (19, '<div><h1>Работа только с определенными клиентами на конкретной территории</h1><div><strong>Описание:</strong> Условие прямо противоречит п. 2 ст. 1033 ГК РФ.</div><div><strong>Уровень риска:</strong> Очень высокий</div></div>', 19);
INSERT INTO public.document_contents (id, content, document_id) VALUES (20, '<div><h1>Несвоевременное обновление франчайзором исключительных прав</h1><div><strong>Описание:</strong> Может привести к утрате доверия франшизы. (например, просрочка регистрации товарного знака).</div><div><strong>Уровень риска:</strong> Высокий</div></div>', 20);
INSERT INTO public.document_contents (id, content, document_id) VALUES (21, '<div><h1>Обязанность франчайзи возмещать убытки за действия третьих лиц</h1><div><strong>Описание:</strong> Условие является односторонним и возлагает достаточно большую ответственность на франчайзи. (ст. 1034 ГК РФ)</div><div><strong>Уровень риска:</strong> Повышенный</div></div>', 21);
INSERT INTO public.document_contents (id, content, document_id) VALUES (22, '<div><h1>Отсутствие механизма возмещения убытков при прекращении действия лицензии франчайзора</h1><div><strong>Описание:</strong> Франчайзи теряет вложения, если франчайзор лишился прав на товарный знак. (ст. 1039 ГК РФ)</div><div><strong>Уровень риска:</strong> Очень высокий</div></div>', 22);
INSERT INTO public.document_contents (id, content, document_id) VALUES (23, '<div><h1>Запрет на участие в управлении бизнесом третьих лиц</h1><div><strong>Описание:</strong> Ограничивает ведение бизнеса наследникам, близким родственникам, членам семьи.</div><div><strong>Уровень риска:</strong> Повышенный</div></div>', 23);
INSERT INTO public.document_contents (id, content, document_id) VALUES (24, '<div><h1>Требование о внесении изменений в помещение/оборудование без компенсации</h1><div><strong>Описание:</strong> Например, обязательный дорогостоящий ремонт каждые 2 года. Высокие затраты. (ст. 1032 ГК РФ)</div><div><strong>Уровень риска:</strong> Высокий</div></div>', 24);
INSERT INTO public.document_contents (id, content, document_id) VALUES (25, '<div><h1>Ограничение на использование киберспортивного бренда вне договора</h1><div><strong>Описание:</strong> Франчайзи не может использовать бренд для стримов, мерча или спонсорства без согласования.</div><div><strong>Уровень риска:</strong> Очень высокий</div></div>', 25);
INSERT INTO public.document_contents (id, content, document_id) VALUES (26, '<div><h1>Обязательное соответствие внешнего вида клуба стандартам франчайзора</h1><div><strong>Описание:</strong> Дорогостоящий ремонт и дизайн помещения, даже если это не влияет на прибыль. Высокие требования к начальному капиталу.</div><div><strong>Уровень риска:</strong> Высокий</div></div>', 26);
INSERT INTO public.document_contents (id, content, document_id) VALUES (27, '<div><h1>Запрет на сотрудничество с другими киберспортивными организациями</h1><div><strong>Описание:</strong> Нельзя проводить турниры с конкурентами или привлекать спонсоров из "черного списка". Риск снижения дополнительного дохода.</div><div><strong>Уровень риска:</strong> Умеренный</div></div>', 27);
INSERT INTO public.document_contents (id, content, document_id) VALUES (28, '<div><h1>Ограничение на субконцессию</h1><div><strong>Описание:</strong> Невозможно передать права третьим лицам без согласия правообладателя.</div><div><strong>Уровень риска:</strong> Умеренный</div></div>', 28);
INSERT INTO public.document_contents (id, content, document_id) VALUES (29, '<div><h1>Обязательное использование только лицензионного ПО</h1><div><strong>Описание:</strong> Закупка дорогих лицензий на игры/софт, даже если есть бесплатные аналоги.</div><div><strong>Уровень риска:</strong> Низкий</div></div>', 29);
INSERT INTO public.document_contents (id, content, document_id) VALUES (30, '<div><h1>Высокие роялти с выручки</h1><div><strong>Описание:</strong> Даже при низкой прибыли франчайзи обязан платить высокие роялти.</div><div><strong>Уровень риска:</strong> Критический</div></div>', 30);


--
-- TOC entry 4918 (class 0 OID 24594)
-- Dependencies: 218
-- Data for Name: documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (30, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Высокие роялти с выручки');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (29, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Обязательное использование только лицензионного ПО');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (28, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Ограничение на субконцессию');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (27, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Запрет на сотрудничество с другими киберспортивными организациями');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (26, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Обязательное соответствие внешнего вида клуба стандартам франчайзора');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (25, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Ограничение на использование киберспортивного бренда вне договора');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (24, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Требование о внесении изменений в помещение/оборудование без компенсации');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (23, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Запрет на участие в управлении бизнесом третьих лиц');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (22, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Отсутствие механизма возмещения убытков при прекращении действия лицензии франчайзора');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (21, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Обязанность франчайзи возмещать убытки за действия третьих лиц');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (20, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Несвоевременное обновление франчайзором исключительных прав');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (19, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Работа только с определенными клиентами на конкретной территории');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (18, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Аудит деятельности франчайзи');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (17, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Отсутствие компенсации за улучшения, внесенные франчайзи');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (16, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Непропорциональное распределение рекламных расходов');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (15, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Запрет на ведение аналогичного бизнеса после прекращения договора');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (14, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Отсутствие четкого порядка разрешения споров');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (13, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Штрафы за невыполнение плановых показателей');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (12, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Автоматическое продление договора без согласия франчайзи');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (11, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Обязанность закупать товары/сырье только у франчайзора или его партнеров по завышенным ценам');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (10, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Запрет на самостоятельное изменение ценообразования');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (9, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Запрет на оспаривание товарного знака или технологии франчайзора');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (8, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Ограничение ответственности франчайзора за недобросовестные действия');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (7, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Одностороннее изменение франчайзором условий договора');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (6, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Запрет на оспаривание исключительных прав франчайзора');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (5, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Отсутствие четких критериев качества товаров/услуг');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (4, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Обязанность соблюдать стандарты бизнес-процессов без возможности адаптации под локальный рынок');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (3, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Штрафные санкции за односторонний отказ от договора');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (2, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Ограничения на ведение самостоятельной деятельности');
INSERT INTO public.documents (id, created_at, updated_at, doc_type, title) VALUES (1, '2025-04-14 15:39:06.039992', '2025-04-14 15:39:06.039992', 'Риск', 'Отсутствие гарантий исключительности права использования франшизы');


--
-- TOC entry 4922 (class 0 OID 24619)
-- Dependencies: 222
-- Data for Name: statistics; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 4931 (class 0 OID 0)
-- Dependencies: 219
-- Name: document_contents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.document_contents_id_seq', 29, true);


--
-- TOC entry 4932 (class 0 OID 0)
-- Dependencies: 217
-- Name: documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.documents_id_seq', 33, true);


--
-- TOC entry 4933 (class 0 OID 0)
-- Dependencies: 221
-- Name: statistics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.statistics_id_seq', 1, false);


--
-- TOC entry 4763 (class 2606 OID 24612)
-- Name: document_contents document_contents_document_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_contents
    ADD CONSTRAINT document_contents_document_id_key UNIQUE (document_id);


--
-- TOC entry 4765 (class 2606 OID 24610)
-- Name: document_contents document_contents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_contents
    ADD CONSTRAINT document_contents_pkey PRIMARY KEY (id);


--
-- TOC entry 4759 (class 2606 OID 24601)
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- TOC entry 4761 (class 2606 OID 24634)
-- Name: documents documents_title_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_title_key UNIQUE (title);


--
-- TOC entry 4767 (class 2606 OID 24627)
-- Name: statistics statistics_document_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statistics
    ADD CONSTRAINT statistics_document_id_key UNIQUE (document_id);


--
-- TOC entry 4769 (class 2606 OID 24625)
-- Name: statistics statistics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statistics
    ADD CONSTRAINT statistics_pkey PRIMARY KEY (id);


--
-- TOC entry 4770 (class 2606 OID 24613)
-- Name: document_contents document_contents_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_contents
    ADD CONSTRAINT document_contents_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id) ON DELETE CASCADE;


--
-- TOC entry 4771 (class 2606 OID 24628)
-- Name: statistics statistics_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statistics
    ADD CONSTRAINT statistics_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id) ON DELETE CASCADE;


-- Completed on 2025-04-14 15:52:17

--
-- PostgreSQL database dump complete
--

