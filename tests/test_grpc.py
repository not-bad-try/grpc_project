import pytest
import grpc
from concurrent import futures
import time
from db.database import create_database_and_table
import server.generated.data_pb2 as data_pb2
import server.generated.data_pb2_grpc as data_pb2_grpc
from server.grpc_server import DataServiceServicer

@pytest.fixture(scope="module")
def grpc_server():
    session = create_database_and_table()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_pb2_grpc.add_DataServiceServicer_to_server(DataServiceServicer(session), server)
    port = server.add_insecure_port('[::]:50051')
    server.start()
    yield server
    server.stop(0)

def test_send_data(grpc_server):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = data_pb2_grpc.DataServiceStub(channel)

        packet = data_pb2.DataPacket(
            PacketTimestamp=int(time.time()),
            PacketSeqNum=1,
            NRecords=2,
            PacketData=[
                data_pb2.Data(Decimal1=1.1, Decimal2=2.2, Decimal3=3.3, Decimal4=4.4, RecordTimestamp=int(time.time())),
                data_pb2.Data(Decimal1=5.5, Decimal2=6.6, Decimal3=7.7, Decimal4=8.8, RecordTimestamp=int(time.time()))
            ]
        )

        response = stub.SendDataPacket(packet)
        assert response.success is True
        assert response.message == "Data saved successfully"
