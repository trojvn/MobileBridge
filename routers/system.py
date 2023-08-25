import os
import subprocess

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/system", tags=["system"])


@router.post("/os")
def os(cmd: str):
    try:
        result_code = os.system(cmd)
        return {"result": True, "code": result_code}
    except Exception as e:
        raise HTTPException(500, detail={"msg": str(e), "msg_type": str(type(e))})


@router.post("/subprocess/run")
def subprocess_run(cmd: str):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.stdout.decode("utf-8")
    stderr = result.stderr.decode("utf-8")
    return {"result": True, "stdout": stdout, "stderr": stderr}
