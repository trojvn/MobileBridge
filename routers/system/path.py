import contextlib
import os
import shutil
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(prefix="/system/path", tags=["path"])


@router.get("/mkdir/")
def system_path_mkdir(path: str) -> dict:
    p = Path(path)
    p.parent.parent.mkdir(exist_ok=True)
    p.parent.mkdir(exist_ok=True)
    p.mkdir(exist_ok=True)
    return {"result": True}


@router.get("/remove/")
def system_path_remove(path: str) -> dict:
    p = Path(path)
    shutil.rmtree(p, ignore_errors=True)
    with contextlib.suppress(Exception):
        os.remove(p)
    return {"result": True}


@router.get("/exists/")
def system_path_exists(path: str) -> dict:
    return {"result": Path(path).exists()}


@router.get("/move/")
def system_path_move(path: str, dst_path: str) -> dict:
    with contextlib.suppress(Exception):
        shutil.move(path, dst_path)
        return {"result": True}
    return {"result": False}


@router.get("/walk/")
def system_path_walk(path: str) -> dict:
    p = Path(path)
    files, dirs = [], []
    try:
        for item in p.iterdir():
            if item.is_file():
                files.append(str(item))
            if item.is_dir():
                dirs.append(str(item))
        a = files + dirs
        return {"result": True, "files": files, "dirs": dirs, "all": a}
    except Exception:
        return {"result": False, "files": [], "dirs": [], "all": []}
