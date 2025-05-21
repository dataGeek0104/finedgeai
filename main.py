import os
import asyncio
from uvicorn import Config, Server


async def serve():
    port = int(os.getenv("CLI_PORT", 8000))  # default to 8000 if not set
    config = Config(
        "app.app:app",  # module:path to your FastAPI `app`
        host="localhost",
        port=port,
        reload=True,  # only for dev; disable in prod
    )
    server = Server(config)
    await server.serve()  # this is now non-blocking within asyncio


if __name__ == "__main__":
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        pass
