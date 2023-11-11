import contextlib
from typing import Optional

from pyaxmlparser import APK


def get_pkg_by_apk(apk_path: str) -> Optional[str]:
    with contextlib.suppress(Exception):
        return APK(apk_path).packagename


def check_apk(apk_path: str) -> Optional[bool]:
    with contextlib.suppress(Exception):
        return APK(apk_path).is_valid_APK()
