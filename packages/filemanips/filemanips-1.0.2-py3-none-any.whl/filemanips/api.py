import enum
import logging
import os
import shutil


class FileManipFunctions(enum.IntEnum):
    MOVE = 0
    COPY = 1


LOGGER = logging.getLogger(__name__)


def move(src, dest):
    """Move a file or folder to a destination. If the destination does not exist, including any folders along the way, it will be created

    Args:
        src (str): Source file/folder
        dest (str): Destination file/folder
    """
    _file_manip_base_function(src, dest, FileManipFunctions.MOVE)


def copy(src, dest):
    """Copy a file or folder to a destination. If the destination does not exist, including any folders along the way, it will be created

    Args:
        src (str): Source file/folder
        dest (str): Destination file/folder

    Raises:
        FileNotFoundError: If the source file is not found
        FileExistsError: If the destination is a folder but the parameter does not have a separator at the end of it
    """
    _file_manip_base_function(src, dest, FileManipFunctions.COPY)


def _file_manip_base_function(src, dest, func):
    specified_dest_is_folder = dest.endswith(os.sep)
    if not os.path.exists(src):
        raise FileNotFoundError(f"{src} does not exist")
    elif os.path.isdir(dest) and not specified_dest_is_folder:
        raise FileExistsError(
            f"{dest} is a directory; specify it with a slash in the function call")
    elif not os.path.exists(dest):
        d = dest.split(os.sep)
        for i in range(1, len(d)):
            full_path = os.path.join(*d[0:i])
            if dest.startswith(os.sep):
                full_path = f"{os.sep}{full_path}"
            if not os.path.exists(full_path):
                if i != len(d) or specified_dest_is_folder:
                    os.makedirs(full_path, exist_ok=True)
                    LOGGER.info(f"Created {full_path}{os.sep}")
    if specified_dest_is_folder:
        dest = dest + os.path.basename(src)
    if func == FileManipFunctions.MOVE:
        shutil.move(src, dest)
        LOGGER.info(f"{src} -> {dest}")
    elif func == FileManipFunctions.COPY:
        if os.path.isdir(src):
            shutil.copytree(src, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dest)
        LOGGER.info(f"{src} => {dest}")


def delete(src):
    """Delete a file or folder

    Args:
        src (str): File/folder to delete
    """
    if os.path.isdir(src):
        shutil.rmtree(src)
    else:
        os.remove(src)
    LOGGER.info(f"Deleted {src}")
