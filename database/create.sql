CREATE TABLE Roles (
    id_role INTEGER PRIMARY KEY,
    role_name varchar(50)
);

CREATE TABLE Employees (
    id_employee INTEGER PRIMARY KEY,
    last_name varchar(70),
    first_name varchar(70),
    middle_name varchar(70),
    phone_number varchar(20),
    email varchar(50),
    password varchar(50),
    ratting INTEGER,
    experience INTEGER,
    id_role INTEGER,
    FOREIGN KEY (id_role) REFERENCES Roles(id_role)
);

CREATE TABLE Clients (
    id_client INTEGER PRIMARY KEY,
    last_name varchar(70),
    first_name varchar(70),
    middle_name varchar(70),
    phone_number varchar(20),
    email varchar(60),
    password varchar(50),
    sex char(1),
    age INTEGER,
    id_role INTEGER,
    FOREIGN KEY (id_role) REFERENCES Roles(id_role)
);

CREATE TABLE Reviews (
    id_review INTEGER PRIMARY KEY,
    id_client INTEGER,
    content TEXT,
    FOREIGN KEY (id_client) REFERENCES Clients(id_client)
);

CREATE TABLE Requests (
    id_requst INTEGER PRIMARY KEY,
    id_client INTEGER,
    id_employee INTEGER,
    Description TEXT,
    Deadline DATE,
    status varchar(30),
    FOREIGN KEY (id_client) REFERENCES Clients(id_client),
    FOREIGN KEY (id_employee) REFERENCES Employees(id_employee)
);


-- Заполнение таблицы Roles
INSERT INTO Roles (role_name) VALUES ('Сотрудник');
INSERT INTO Roles (role_name) VALUES ('Клиент');

-- Заполнение таблицы Employees
INSERT INTO Employees (last_name, first_name, middle_name, phone_number, ratting, experience, id_role)
VALUES ('Иванов', 'Иван', 'Иванович', '123-456-789', 5, 3, 2);

-- Заполнение таблицы Clients
INSERT INTO Clients (last_name, first_name, middle_name, phone_number, email, sex, age, id_role)
VALUES ('Петрова', 'Анна', 'Сергеевна', '987-654-321', 'anna@example.com', 'Ж', 25, 1);

-- Заполнение таблицы Reviews
INSERT INTO Reviews (id_client, content) VALUES (1, 'Отличный сервис!');

-- Заполнение таблицы Requests
INSERT INTO Requests (id_client, id_employee, Description, Deadline)
VALUES (1, 1, 'Исправить мою проблему', '2023-12-31');
