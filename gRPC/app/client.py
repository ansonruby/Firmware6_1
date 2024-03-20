import setup
from lib.Lib_Settings import Set_Rele
from lib.Fun_Dispositivo import Get_ID_Dispositivo
from lib.Lib_Speaker import send_speaker_msg
import time
import asyncio
import grpc
import sirena_pb2
import sirena_pb2_grpc


async def get_grpc_stream():
    uuid = Get_ID_Dispositivo()
    channel_options = [
        ("grpc.keepalive_time_ms", 60000),
        ("grpc.keepalive_timeout_ms", 50000),
        ("grpc.keepalive_permit_without_calls", 1),
        ("grpc.http2.max_pings_without_data", 5),
    ]
    async with grpc.aio.secure_channel(
        "communication.fusepong.com",
        grpc.ssl_channel_credentials(),
        options=channel_options
    ) as channel:

        try:
            stub = sirena_pb2_grpc.SirenaServiceStub(channel)
            async for response in stub.SendEvents(sirena_pb2.Channel(uuid=uuid)):
                send_speaker_msg(
                    {
                        "priority": response.priority,
                        "message": response.message,
                        "audio": response.audio
                    }
                )
        except Exception as e:
            print(e)


async def main():
    while True:
        await get_grpc_stream()

if __name__ == "__main__":
    while True:
        asyncio.run(main())
