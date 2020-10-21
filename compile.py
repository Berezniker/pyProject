from config import PROJECT_PATH, APP_NAME, ICON_APP_PATH
import shutil
import time
import os


def compile_project() -> None:
    """
    Compiles and builds the project
    documentation: https://pyinstaller.readthedocs.io/en/stable/index.html
    options: https://pyinstaller.readthedocs.io/en/stable/usage.html

    :return: None
    """
    command = f"""
        pyinstaller
            --distpath {PROJECT_PATH}
            --clean
            --log-level ERROR
            --onefile
            --name {APP_NAME}
            --icon {ICON_APP_PATH}
        {os.path.join(PROJECT_PATH, "main.py")}
    """
    # TODO add --noconsole
    command = " ".join(command.split())  # must be in one line

    compile_time = time.time()
    status_code = os.system(command)
    compile_time = time.strftime('%M:%S', time.gmtime(round(time.time() - compile_time)))
    app_size = os.path.getsize(os.path.join(PROJECT_PATH, f"{APP_NAME}.exe")) >> 20

    if status_code == 0:
        shutil.rmtree(os.path.join(PROJECT_PATH, "build"))
        os.remove(os.path.join(PROJECT_PATH, f"{APP_NAME}.spec"))

    print(f"Compile time: {compile_time}",
          f"    App size: {app_size} MB", sep='\n')
    return


if __name__ == '__main__':
    print("Run!")
    compile_project()
    print("End of run.")
