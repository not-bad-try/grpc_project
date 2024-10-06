import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc
import json
import psycopg2
from datetime import datetime

# Загрузка конфигурационного файла
def load_config():
    with open('server_config.json', 'r') as f:
        return json.load(f)

# Класс сервера
class DemoService(service_pb2_grpc.DemoServiceServicer):
    def __init__(self):
        # Подключение к базе данных PostgreSQL
        self.conn = psycopg2.connect(dbname="grpc_db", user="grpc_user", password="grpc_pass", host="localhost")

    def sendData(self, request, context):
        cursor = self.conn.cursor()

        for i, record in enumerate(request.PacketData):
            cursor.execute("""
                INSERT INTO grpc_data (PacketSeqNum, RecordSeqNum, PacketTimestamp, Decimal1, Decimal2, Decimal3, Decimal4, RecordTimestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                request.PacketSeqNum,
                i,
                datetime.fromisoformat(request.PacketTimestamp),
                record.Decimal1,
                record.Decimal2,
                record.Decimal3,
                record.Decimal4,
                datetime.fromisoformat(record.Timestamp)
            ))

        self.conn.commit()
        return service_pb2.DataResponse(message="Данные успешно сохранены")

# Функция для запуска сервера
def serve():
    config = load_config()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_DemoServiceServicer_to_server(DemoService(), server)
    server.add_insecure_port(f'[::]:{config["gRPCServerPort"]}')
    print(f"Сервер запущен на порту {config['gRPCServerPort']}...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
