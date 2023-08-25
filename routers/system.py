import os
import subprocess
from subprocess import PIPE, Popen

from fastapi import APIRouter, HTTPException

from processes import Process, PopenStore, find_processes

router = APIRouter(prefix="/system", tags=["system"])


@router.post("/os")
async def os(cmd: str):
    try:
        result_code = os.system(cmd)
        return {"result": True, "code": result_code}
    except Exception as e:
        raise HTTPException(500, detail={"msg": str(e), "msg_type": str(type(e))})


@router.post("/subprocess/run")
async def subprocess_run(cmd: str):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=PIPE)
        stdout = result.stdout.decode("utf-8")
        stderr = result.stderr.decode("utf-8")
        return {"result": True, "stdout": stdout, "stderr": stderr}
    except Exception as e:
        raise HTTPException(500, detail={"msg": str(e), "msg_type": str(type(e))})


@router.post("/subprocess/popen")
async def subprocess_popen(cmd: str):
    try:
        result = Popen(cmd, stdout=subprocess.PIPE, stderr=PIPE)
        process = Process(cmd, result)
        PopenStore.processes.append(process)
        return {"result": True}
    except Exception as e:
        raise HTTPException(500, detail={"msg": str(e), "msg_type": str(type(e))})


@router.post("/subprocess/pclose")
async def subprocess_pclose(cmd: str):
    for process in find_processes(cmd):
        process.instance.terminate()
    return {"result": True}
