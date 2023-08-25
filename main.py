import colorama

# noinspection PyPackageRequirements
import uvicorn
from fastapi import FastAPI

from routers import systemrouter

colorama.init()
app = FastAPI(title="MobileBridge")

app.include_router(systemrouter)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8020)


if __name__ == "__main__":
    main()
