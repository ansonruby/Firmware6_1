import setup
import asyncio
import grpc
import sirena_pb2
import sirena_pb2_grpc


async def run():
    async with grpc.aio.insecure_channel("192.168.0.51:3000") as channel:
        stub = sirena_pb2_grpc.SirenaServiceStub(channel)

        async for response in stub.SirenaService(
            sirena_pb2_grpc.Chanel(uuid="1234")
        ):
            print(
                "Greeter client received from async generator: "
                + response.message
            )

        while True:
            response = await hello_stream.read()
            if response == grpc.aio.EOF:
                break
            print(
                "Greeter client received from direct read: " + response.message
            )


if __name__ == "__main__":
    # asyncio.run(run())
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(run())
