import time

import colorama
import uvicorn
from fastapi import FastAPI

from routers import systemrouter
from tools import Kitty, load_tunnel_data, create_tunnel_port, close_process

colorama.init()
app = FastAPI(title="MobileBridge")

app.include_router(systemrouter)


def main():
    port = 8020
    data = load_tunnel_data()
    close_process("m_kitty.exe")
    time.sleep(3)
    kitty_fpath = create_tunnel_port(port)
    with Kitty(kitty_fpath, data.password, data.port):
        uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
