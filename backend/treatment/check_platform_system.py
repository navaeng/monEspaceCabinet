import platform


def check_platform_system():
    system_platform = platform.system()

    if system_platform == "Windows":
        filename = "nava_last_version.exe"
    elif system_platform == "Darwin":
        filename = "nava_last_version.dmg"
    elif system_platform == "Linux":
        filename = "nava_last_version.deb"
    else:
        raise ValueError(f"Unsupported platform: {system_platform}")
    return filename, system_platform
