# gRPC Data Transfer Project

Этот проект реализует gRPC-сервер и клиента для передачи данных в формате пакетов и сохранения их в базу данных PostgreSQL с использованием SQLAlchemy.


## Установка необходимых пакетов на Ubuntu

Для работы проекта необходимо установить следующие пакеты на Ubuntu:

sudo apt update
sudo apt install python3 python3-pip python3-dev libpq-dev postgresql postgresql-contrib

## Установка зависимостей Python
Убедитесь, что у вас установлен Python 3 и pip. Затем установите необходимые зависимости:

pip install -r requirements.txt
Настройка PostgreSQL
Запустите PostgreSQL и создайте базу данных:

sudo -u postgres psql
CREATE DATABASE grpc_db;
\q

Генерация gRPC файлов
Сгенерируйте gRPC файлы из файла data.proto:
python -m grpc_tools.protoc -I./server --python_out=./server/generated --grpc_python_out=./server/generated ./server/data.proto

# Запуск проекта

Откройте терминал и перейдите в корневую директорию проекта.

## Запустите gRPC сервер:
python server/grpc_server.py
Запуск клиента
Откройте другой терминал и снова перейдите в корневую директорию проекта.

## Запустите клиент:
python client/grpc_client.py
Проверка данных в базе данных
Чтобы проверить, что данные были успешно сохранены, подключитесь к базе данных и выполните:

sudo -u postgres psql grpc_db
SELECT * FROM grpc_data;

## Запуск тестов
Для запуска тестов используйте pytest:

pytest tests/test_grpc.py
