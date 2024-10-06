import pytest
import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc
from server import DemoService
from unittest import mock
import psycopg2
from datetime import datetime


@pytest.fixture(scope="module")
def grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_DemoServiceServicer_to_server(DemoService(), server)
    port = server.add_insecure_port('[::]:50052')  # Используем другой порт для тестирования
    server.start()
    yield f'localhost:{port}'
    server.stop(0)

@pytest.fixture
def db_connection():
    conn = psycopg2.connect(dbname="grpc_db", user="grpc_user", password="grpc_pass", host="localhost")
    cursor = conn.cursor()
    yield cursor
    conn.close()

# Тест для отправки данных и проверки их сохранения
def test_send_data(grpc_server, mocker, db_connection):
    mocker.patch.object(db_connection.connection, "commit")

    with grpc.insecure_channel(grpc_server) as channel:
        stub = service_pb2_grpc.DemoServiceStub(channel)

        timestamp = datetime.now().isoformat()
        data_packet = service_pb2.DataPacket(
            PacketTimestamp=timestamp,
            PacketSeqNum=1,
            NRecords=1,
            PacketData=[
                service_pb2.Data(
                    Decimal1=1.1,
                    Decimal2=2.2,
                    Decimal3=3.3,
                    Decimal4=4.4,
                    Timestamp=timestamp
                )
            ]
        )

        response = stub.sendData(data_packet)

        assert response.message == "Данные успешно сохранены"

        db_connection.execute("""
            SELECT * FROM grpc_data WHERE PacketSeqNum = %s AND RecordSeqNum = %s
        """, (1, 0))

        result = db_connection.fetchone()

        assert result is not None
        assert result[0] == 1  # PacketSeqNum
        assert result[1] == 0  # RecordSeqNum
        assert result[2] == datetime.fromisoformat(timestamp)  # PacketTimestamp
        assert result[3] == 1.1  # Decimal1
        assert result[4] == 2.2  # Decimal2
        assert result[5] == 3.3  # Decimal3
        assert result[6] == 4.4  # Decimal4
        assert result[7] == datetime.fromisoformat(timestamp)  # RecordTimestamp
