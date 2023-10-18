from typing import Literal

from fastapi import APIRouter

from android_tools import get_package_name_by_apk, check_apk

router = APIRouter(prefix="/android", tags=["android"])

GetActions = Literal["packagename", "checkapk"]


@router.get("/")
def android(action: GetActions, apk_path: str):
    if action == "packagename":
        if packagename := get_package_name_by_apk(apk_path):
            return {"result": True, "packagename": packagename}
    elif action == "checkapk":
        if status := check_apk(apk_path):
            return {"result": True, "checkapk": status}
    return {"result": False}
