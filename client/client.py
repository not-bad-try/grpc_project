import grpc
import time
import json
from datetime import datetime
import server.generated.data_pb2 as data_pb2
import server.generated.data_pb2_grpc as data_pb2_grpc

with open("client/client_config.json") as f:
    config = json.load(f)

def generate_packet(seq_num, records_in_packet):
    packet_timestamp = int(time.time())
    data_list = []
    for i in range(records_in_packet):
        record_timestamp = int(time.time())
        data = data_pb2.Data(
            Decimal1=round(1.1 * (i + 1), 2),
            Decimal2=round(2.2 * (i + 1), 2),
            Decimal3=round(3.3 * (i + 1), 2),
            Decimal4=round(4.4 * (i + 1), 2),
            RecordTimestamp=record_timestamp,
        )
        data_list.append(data)
    return data_pb2.DataPacket(
        PacketTimestamp=packet_timestamp,
        PacketSeqNum=seq_num,
        NRecords=records_in_packet,
        PacketData=data_list,
    )

def run():
    with grpc.insecure_channel(f"{config['gRPCServerAddr']}:{config['gRPCServerPort']}") as channel:
        stub = data_pb2_grpc.DataServiceStub(channel)
        for seq_num in range(1, config['TotalPackets'] + 1):
            packet = generate_packet(seq_num, config['RecordsInPacket'])
            response = stub.SendDataPacket(packet)
            print(f"Packet {seq_num} sent. Server response: {response.message}")
            time.sleep(config['TimeInterval'])

if __name__ == "__main__":
    run()
