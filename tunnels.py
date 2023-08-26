import contextlib
import json
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Optional, NamedTuple

kitty_path = "kitty"
kitty_exe = "kitty.exe"

tunnel = Path("tunnel.json")
args = '-auto-store-sshkey -load "Default Settings"'


class TunnelData(NamedTuple):
    password: str
    port: int


def load_tunnel_data() -> Optional[TunnelData]:
    with tunnel.open("r", encoding="utf-8") as f:
        json_data = json.load(f)
    with contextlib.suppress(Exception):
        return TunnelData(json_data["pw"], int(json_data["port"]))
    raise ValueError(f"Не удалось загрузить {tunnel.name}")


class Kitty:
    def __init__(self, password: str, port: int):
        self.__kitty: Optional[Popen[bytes]] = None
        self.__password = password
        self.__port = port

    def kitty_start(self):
        pw = self.__password
        port = self.__port
        cmd = f"{kitty_path}/{kitty_exe} -pw {pw} -P {port} {args}"
        self.__kitty = Popen(
            cmd,
            cwd=kitty_path,
            stdout=PIPE,
            stderr=PIPE,
        )

    def kitty_stop(self):
        if self.__kitty:
            self.__kitty.terminate()
            self.__kitty.kill()
            self.__kitty = None

    def __enter__(self):
        self.kitty_start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kitty_stop()
