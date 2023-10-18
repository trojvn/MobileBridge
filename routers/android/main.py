import contextlib
from typing import Optional, Literal

from fastapi import APIRouter
from pyaxmlparser import APK

router = APIRouter(prefix="/android", tags=["android"])

GetActions = Literal["packagename"]


@router.get("/")
def android(action: GetActions, apk_path: str = None):
    if action == "packagename":
        if packagename := get_package_name_by_apk(apk_path):
            return {"result": True, "packagename": packagename}
        return {"result": False}
    return {"result": False}


def get_package_name_by_apk(apk_path: str) -> Optional[str]:
    with contextlib.suppress(Exception):
        return APK(apk_path).packagename
