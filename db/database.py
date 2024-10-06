from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, GRPCData

# Создание подключения к базе данных
def create_database_and_table():
    engine = create_engine('postgresql://your_username:your_password@localhost/grpc_db')
    
    # Создание базы данных, если её нет
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    return session

# Функция для сохранения данных
def save_packet_data(session, packet_seq_num, packet_timestamp, packet_data):
    for idx, record in enumerate(packet_data):
        grpc_data = GRPCData(
            PacketSeqNum=packet_seq_num,
            RecordSeqNum=idx + 1,
            PacketTimestamp=packet_timestamp,
            Decimal1=record.Decimal1,
            Decimal2=record.Decimal2,
            Decimal3=record.Decimal3,
            Decimal4=record.Decimal4,
            RecordTimestamp=record.RecordTimestamp
        )
        session.add(grpc_data)
    session.commit()

