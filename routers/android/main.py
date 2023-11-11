from typing import Literal

from fastapi import APIRouter

from android_tools import get_pkg_by_apk, check_apk

router = APIRouter(prefix="/android", tags=["android"])

GetActions = Literal["pkg_name", "check_apk"]


@router.get("/")
def android(action: GetActions, apk_path: str):
    if action == "pkg_name":
        if pkg_name := get_pkg_by_apk(apk_path):
            return {"result": True, "pkg_name": pkg_name}
    elif action == "check_apk":
        if status := check_apk(apk_path):
            return {"result": True, "check_apk": status}
    return {"result": False}
