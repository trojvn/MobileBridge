import contextlib
import os
import shutil
import subprocess
from pathlib import Path
from subprocess import PIPE, Popen

from dotenv import load_dotenv
from fastapi import APIRouter

from processes import Process, PopenStore, find_processes

load_dotenv()
DEBUG = os.getenv("DEBUG", False)

router = APIRouter(prefix="/system", tags=["system"])


@router.post("/os")
async def os_system(cmd: str):
    try:
        result_code = os.system(cmd)
        return {"result": True, "code": result_code}
    except Exception as e:
        print(e)
        return {"result": False, "msg": str(e)}


@router.post("/subprocess/run")
async def subprocess_run(cmd: str, cwd: str = "."):
    try:
        result = subprocess.run(cmd, cwd=cwd, stdout=PIPE, stderr=PIPE)
        stdout = result.stdout.decode("windows-1251")
        stderr = result.stderr.decode("windows-1251")
        return {"result": True, "stdout": stdout, "stderr": stderr}
    except Exception as e:
        print(e)
        return {"result": False, "msg": str(e)}


@router.post("/subprocess/popen")
async def subprocess_popen(cmd: str, cwd: str = "."):
    try:
        with open(os.devnull, "w") as null:
            if DEBUG:
                result = Popen(cmd, cwd=cwd)
            else:
                result = Popen(cmd, cwd=cwd, stdout=null, stderr=null)
        process = Process(cmd, result)
        PopenStore.processes.append(process)
        return {"result": True}
    except Exception as e:
        print(e)
        return {"result": False, "msg": str(e)}


@router.post("/subprocess/pclose")
async def subprocess_pclose(cmd: str):
    for process in find_processes(cmd):
        process.instance.terminate()
        process.instance.kill()
        PopenStore.processes.remove(process)
    return {"result": True}


@router.get("/subprocess/get_processes")
async def get_subprocesses() -> list[str]:
    return [proc.cmd for proc in PopenStore.processes]


@router.post("/path/mkdir")
async def path_mkdir(path: str):
    p = Path(path)
    p.parent.parent.mkdir(exist_ok=True)
    p.parent.mkdir(exist_ok=True)
    p.mkdir(exist_ok=True)
    return {"result": True}


@router.post("/path/remove")
async def path_remove(path: str):
    p = Path(path)
    shutil.rmtree(p, ignore_errors=True)
    with contextlib.suppress(Exception):
        os.remove(p)
    return {"result": True}


@router.get("/path/exists")
async def path_exists(path: str):
    p = Path(path)
    if p.exists():
        return {"result": True}
    return {"result": False}
