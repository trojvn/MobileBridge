from dataclasses import dataclass
from subprocess import Popen


@dataclass
class Process:
    cmd: str
    instance: Popen[bytes]


class PopenStore:
    processes: list[Process] = []


def find_processes(cmd: str) -> list[Process]:
    """Поиск всех совпадений из процессов по отправленной команде из cmd"""
    return [process for process in PopenStore.processes if process.cmd == cmd]
