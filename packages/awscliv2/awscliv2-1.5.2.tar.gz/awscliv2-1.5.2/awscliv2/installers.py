"""
AWS CLI v2 installers.
"""
import os
import platform
import shutil
from io import StringIO
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from urllib.request import urlopen
from zipfile import ZipFile

from awscliv2.constants import LINUX_ARM_URL, LINUX_X86_64_URL, MACOS_URL
from awscliv2.exceptions import InstallError
from awscliv2.interactive_process import InteractiveProcess
from awscliv2.logger import get_logger


def download_file(url: str, target: Path) -> None:
    """
    Download file from `url` to `target` path.
    """
    get_logger().info(f"Downloading package from {url} to {target}")
    with urlopen(url) as f:
        target.write_bytes(f.read())


def install_macos() -> None:
    """
    Install AWS CLI v2 for MacOS.
    """
    logger = get_logger()
    logger.info("Installing AWS CLI v2 for MacOS")
    install_path = Path.home() / "aws-cli"
    if install_path.exists():
        logger.info(f"Removing {install_path}")
        shutil.rmtree(install_path)

    with NamedTemporaryFile("w+", suffix=".pkg") as f_obj:
        package_path = Path(f_obj.name)
        download_file(MACOS_URL, package_path)
        logger.info(f"Installing {package_path} to {install_path}")
        InteractiveProcess(
            [
                "installer",
                "-pkg",
                package_path.as_posix(),
                "-target",
                install_path.as_posix(),
                "-applyChoiceChangesXML",
                "choices.xml",
            ]
        )
    logger.info("Now awsv2 will use this installed version")
    logger.info("Running now to check installation: awsv2 --version")


def install_linux_x86_64() -> None:
    """
    Install AWS CLI v2 for Linux x86_64.
    """
    install_linux(LINUX_X86_64_URL)


def install_linux_arm() -> None:
    """
    Install AWS CLI v2 for Linux ARM.
    """
    install_linux(LINUX_ARM_URL)


def install_linux(url) -> None:
    """
    Install AWS CLI v2 for Linux from `url`.
    """
    logger = get_logger()
    logger.info("Installing AWS CLI v2 for Linux")
    temp_dir = Path(TemporaryDirectory().name)
    install_path = Path.home() / ".awscliv2"
    if install_path.exists():
        logger.info(f"Removing {install_path}")
        shutil.rmtree(install_path)

    bin_path = install_path / "binaries"
    with NamedTemporaryFile("w+", suffix=".zip") as f_obj:
        package_path = Path(f_obj.name)
        download_file(url, package_path)
        logger.info(f"Extracting {package_path} to to {temp_dir}")
        with ZipFile(package_path, "r") as zip_obj:
            zip_obj.extractall(
                temp_dir,
            )

    installer_path = temp_dir / "aws" / "install"
    os.chmod(installer_path, 0o744)
    os.chmod(temp_dir / "aws" / "dist" / "aws", 0o744)
    logger.info(f"Installing {installer_path} to {install_path}")
    output = StringIO()
    return_code = InteractiveProcess(
        [
            installer_path.as_posix(),
            "-i",
            install_path.as_posix(),
            "-b",
            bin_path.as_posix(),
        ]
    ).run(stdout=output)
    if return_code:
        raise InstallError(f"Installation failed: {output.getvalue()}")
    shutil.rmtree(temp_dir)
    logger.info("Now awsv2 will use this installed version")
    logger.info("Running now to check installation: awsv2 --version")


def install_multiplatform():
    """
    Install AWS CLI v2 for Linux ar MacOS.
    """
    os_platform = platform.system()
    arch = platform.architecture()[0]

    if os_platform == "Darwin":
        return install_macos()
    if os_platform == "Linux" and arch == "64bit":
        return install_linux_x86_64()
    if os_platform == "Linux" and arch == "arm":
        return install_linux_arm()

    raise InstallError(f"{os_platform} {arch} is not supported, use docker version")
