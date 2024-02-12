import colorama
import uvicorn
from fastapi import FastAPI
from tunneller import Kitty, PrepareKitty
from tunneller.credentials import get_credentials

from routers import sprocessrouter, pathrouter

colorama.init()
app = FastAPI(title="MobileBridge")

app.include_router(sprocessrouter)
app.include_router(pathrouter)


def main():
    try:
        data = get_credentials("./tunnel.json")
        rports = [i for i in range(4700, 4799)]
        rports.append(8020)
        PrepareKitty(".", "m_kitty", rports, [])
        with Kitty("./m_kitty/m_kitty.exe", data.port, data.pswd):
            uvicorn.run(app, host="0.0.0.0", port=8020)
    except Exception as e:
        print(e)
    input()


if __name__ == "__main__":
    main()
