import contextlib
import os
import shutil
from pathlib import Path
from typing import Literal

from fastapi import APIRouter

router = APIRouter(prefix="/system/path", tags=["path"])

Actions = Literal["mkdir", "remove", "exists"]


@router.post("/")
async def system_path(action: Actions, path: str):
    p = Path(path)
    if action == "mkdir":
        p.parent.parent.mkdir(exist_ok=True)
        p.parent.mkdir(exist_ok=True)
        p.mkdir(exist_ok=True)
        return {"result": True}
    elif action == "remove":
        shutil.rmtree(p, ignore_errors=True)
        with contextlib.suppress(Exception):
            os.remove(p)
        return {"result": True}
    elif action == "exists":
        if p.exists():
            return {"result": True}
        return {"result": False}
