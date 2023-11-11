import contextlib
import os
import shutil
from pathlib import Path
from typing import Literal, Optional

from fastapi import APIRouter

router = APIRouter(prefix="/system/path", tags=["path"])

Actions = Literal["mkdir", "remove", "move", "exists", "walk"]


@router.post("/")
async def system_path(action: Actions, path: str, dst_path: Optional[str] = None):
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
    elif action == "move":
        while True:
            with contextlib.suppress(Exception):
                shutil.move(path, Path(dst_path))
                return {"result": True}
    elif action == "walk":
        files = []
        dirs = []
        for item in p.iterdir():
            if item.is_file():
                files.append(str(item))
            if item.is_dir():
                dirs.append(str(item))
        a = files + dirs
        return {"result": True, "files": files, "dirs": dirs, "all": a}

    return {"result": False}
