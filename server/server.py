import grpc
from concurrent import futures
import time
import json
from datetime import datetime
from db.database import create_database_and_table, save_packet_data
import server.generated.data_pb2 as data_pb2
import server.generated.data_pb2_grpc as data_pb2_grpc

with open("server/server_config.json") as f:
    config = json.load(f)


class DataServiceServicer(data_pb2_grpc.DataServiceServicer):
    def __init__(self, session):
        self.session = session

    def SendDataPacket(self, request, context):
        packet_seq_num = request.PacketSeqNum
        packet_timestamp = datetime.fromtimestamp(request.PacketTimestamp)
        packet_data = request.PacketData


        save_packet_data(self.session, packet_seq_num, packet_timestamp, packet_data)
        return data_pb2.Status(success=True, message="Data saved successfully")

def serve():
    session = create_database_and_table()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_pb2_grpc.add_DataServiceServicer_to_server(DataServiceServicer(session), server)
    server.add_insecure_port(f"[::]:{config['gRPCServerPort']}")
    server.start()
    print(f"Server started on port {config['gRPCServerPort']}")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()