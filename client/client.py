import grpc
import service_pb2
import service_pb2_grpc
import json
import time
from datetime import datetime
import random

def load_config():
    with open('client_config.json', 'r') as f:
        return json.load(f)

# Генерация пакета данных
def generate_packet(seq_num, records_in_packet):
    packet_data = []
    timestamp = datetime.now().isoformat()
    for _ in range(records_in_packet):
        record = service_pb2.Data(
            Decimal1=random.uniform(0, 100),
            Decimal2=random.uniform(0, 100),
            Decimal3=random.uniform(0, 100),
            Decimal4=random.uniform(0, 100),
            Timestamp=datetime.now().isoformat()
        )
        packet_data.append(record)
    
    return service_pb2.DataPacket(
        PacketTimestamp=timestamp,
        PacketSeqNum=seq_num,
        NRecords=records_in_packet,
        PacketData=packet_data
    )

# Функция отправки данных
def run():
    config = load_config()

    # Устанавливаем соединение с сервером
    with grpc.insecure_channel(f'{config["gRPCServerAddr"]}:{config["gRPCServerPort"]}') as channel:
        stub = service_pb2_grpc.DemoServiceStub(channel)
        
        for packet_seq_num in range(1, config['TotalPackets'] + 1):
            # Генерация пакета данных
            packet = generate_packet(packet_seq_num, config['RecordsInPacket'])
            
            # Отправка данных на сервер
            response = stub.sendData(packet)
            print(f"Ответ от сервера: {response.message}")

            # Задержка между отправкой пакетов
            time.sleep(config['TimeInterval'])

if __name__ == '__main__':
    run()
