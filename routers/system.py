import os
import subprocess
from dataclasses import dataclass

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/system", tags=["system"])


@dataclass
class SubProcess:
    cmd: str
    process: subprocess.Popen


processes: list[SubProcess] = []


@router.post("/os")
async def os(cmd: str):
    try:
        result_code = os.system(cmd)
        return {"result": True, "code": result_code}
    except Exception as e:
        raise HTTPException(500, detail={"msg": str(e), "msg_type": str(type(e))})


@router.post("/subprocess/run")
async def subprocess_run(cmd: str):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.stdout.decode("utf-8")
    stderr = result.stderr.decode("utf-8")
    return {"result": True, "stdout": stdout, "stderr": stderr}


@router.post("/subprocess/popen")
async def subprocess_popen(cmd: str):
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = SubProcess(cmd, result)
    processes.append(process)
    return {"result": True, "stdout": result.stdout, "stderr": result.stderr}
