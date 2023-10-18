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
        return {"result": False}
    elif action == "checkapk":
        apkstatus = check_apk(apk_path)
        return {"result": True, "apkstatus": apkstatus}
    return {"result": False}
