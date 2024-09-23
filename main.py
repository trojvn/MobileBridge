import colorama
import uvicorn
from fastapi import FastAPI
from tunneller import Kitty, PrepareKitty
from tunneller.credentials import get_credentials
from tunneller.kitty.tools import LPort

from routers.system.path import router as pathrouter
from routers.system.sprocess import router as sprocessrouter

colorama.init()
app = FastAPI(title="MobileBridge")

app.include_router(sprocessrouter)
app.include_router(pathrouter)


def main():
    try:
        data = get_credentials("./tunnel.json")
        rports = list(range(4700, 4750))
        rports.append(8020)
        lports = [LPort("mobileapi", 80, 8021)]
        PrepareKitty(data.host, ".", "m_kitty", rports, lports)
        with Kitty("./m_kitty/m_kitty.exe", data.port, data.pswd):
            uvicorn.run(app, host="0.0.0.0", port=8020)
    except Exception as e:
        print(e)
    input()


if __name__ == "__main__":
    main()
