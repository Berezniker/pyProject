from config import PROJECT_PATH, APP_NAME, ICON_APP_PATH
import argparse
import shutil
import time
import os


def add_arguments(argparser) -> None:
    """
    Parse command line arguments

    :return: None
    """
    argparser.add_argument(
        "-k", "--keep-temporary-file",
        dest="keep_temporary_file",
        action="store_true",
        help="save temporary files after compilation"
    )
    return


def compile_project(keep_temporary_file: bool = False) -> None:
    """
    Compiles and builds the project with PyInstaller
    documentation: https://pyinstaller.readthedocs.io/en/stable/index.html
    options: https://pyinstaller.readthedocs.io/en/stable/usage.html

    :return: None
    """
    command = f"""
        pyinstaller
            --distpath {PROJECT_PATH}
            --noconsole
            --clean
            --log-level ERROR
            --onefile
            --name {APP_NAME}
            --icon {ICON_APP_PATH}
            --hidden-import="sklearn.utils._cython_blas"
            --hidden-import="scipy.spatial.transform._rotation_groups"
        {os.path.join(PROJECT_PATH, "main.py")}
    """
    # TODO --paths venv/Lib ?
    command = " ".join(command.split())  # must be in one line

    compile_time = time.time()
    status_code = os.system(command)
    compile_time = round(time.time() - compile_time)
    compile_time = time.strftime('%M:%S', time.gmtime(compile_time))

    app_path = os.path.join(PROJECT_PATH, f"{APP_NAME}.exe")
    app_size = os.path.getsize(app_path) >> 20  # Byte -> MegaByte

    if status_code == 0 and not keep_temporary_file:
        # delete temporary data
        shutil.rmtree(os.path.join(PROJECT_PATH, "build"))
        os.remove(os.path.join(PROJECT_PATH, f"{APP_NAME}.spec"))

    print(f"Compile status: {status_code}",
          f"Compile time  : {compile_time}",
          f"App size      : {app_size} MB", sep='\n')
    return


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Compile project")
    add_arguments(argparser)
    args = argparser.parse_args()
    print("Run!")
    compile_project(args.keep_temporary_file)
    print("End of run.")
