import contextlib
import json
import shutil
import subprocess
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Optional, NamedTuple

TUNNEL = Path("tunnel.json")
ARGS = '-auto-store-sshkey -load "Default Settings"'


class TunnelData(NamedTuple):
    password: str
    port: int


def load_tunnel_data() -> Optional[TunnelData]:
    with TUNNEL.open("r", encoding="utf-8") as f:
        json_data = json.load(f)
    with contextlib.suppress(Exception):
        return TunnelData(json_data["pw"], int(json_data["port"]))
    raise ValueError(f"Не удалось загрузить {TUNNEL.name}")


def create_tunnel_port(port: int) -> Path:
    m_tunnel = Path(f"./m_kitty/{port}/")
    kitty_exe = m_tunnel / "m_kitty.exe"
    if m_tunnel.is_dir():
        shutil.rmtree(m_tunnel, ignore_errors=True)
    shutil.copytree("m_kitty/default/", m_tunnel)
    return kitty_exe


class Kitty:
    def __init__(self, kitty_fpath: Path, password: str, port: int):
        self.__kitty_fpath = kitty_fpath
        self.__kitty: Optional[Popen[bytes]] = None
        self.__password = password
        self.__port = port

    def kitty_start(self):
        pw = self.__password
        port = self.__port
        cmd = f"{self.__kitty_fpath} -pw {pw} -P {port} {ARGS}"
        self.__kitty = Popen(
            cmd,
            cwd=self.__kitty_fpath.parent,
            stdout=PIPE,
            stderr=PIPE,
        )

    def kitty_stop(self):
        if self.__kitty:
            self.__kitty.terminate()
            self.__kitty.kill()
            self.__kitty = None

    def __enter__(self):
        cmd = f"taskkill /f /im {self.__kitty_fpath.name}"
        subprocess.run(cmd, stdout=PIPE, stderr=PIPE)
        self.kitty_start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kitty_stop()
