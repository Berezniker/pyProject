from src.authorization.database import UserDB
import tkinter as tk
import functools
import logging


# link:
# https://docs.python.org/3/library/tk.html
# https://python-scripts.com/tkinter


def one_shot_login(login: str, password: str) -> int:
    db = UserDB()
    ok, problem = db.check_login(
        username=login,
        password=password
    )
    if not ok:
        logging.info(problem)
        logging.info(f"Register a new user: (`{login}`, `{password}`)")
        ok, problem = db.add(
            username=login,
            password=password
        )
        if not ok:
            logging.error(problem)
            return -1

    user_id = db.get_user_id(
        username=login,
        password=password
    )
    return user_id


def login(mode: str) -> int:
    """
    User data verification

    :param mode: "LogIn" / "Register"
    :return: User ID
    """
    # connect to database
    db = UserDB()
    func = db.check_login if mode == 'LogIn' else db.add

    # create window
    master = tk.Tk()
    master.title(f"{mode} Form")
    # get monitor resolution
    w = master.winfo_screenwidth()
    h = master.winfo_screenheight()
    # set window position in center
    master.geometry(f'220x150+{w // 2 - 110}+{h // 2 - 100}')
    # make window non-resizable
    master.resizable(False, False)
    user_id = -1
    success = False

    def success_exit() -> None:
        nonlocal user_id
        master.destroy()
        user_id = db.get_user_id(
            username=username.get(),
            password=password.get()
        )
        return

    # username label and text entry box
    tk.Label(
        master=master,
        text="User Name"
    ).grid(
        row=0, column=0,
        padx=10, pady=10,
        sticky=tk.W
    )
    username = tk.StringVar()
    entry_username = tk.Entry(
        master=master,
        textvariable=username
    )
    entry_username.grid(
        row=0, column=1,
        columnspan=2
    )

    # password label and text entry box
    tk.Label(
        master=master,
        text="Password"
    ).grid(
        row=1, column=0,
        padx=10, pady=10,
        sticky=tk.W
    )
    password = tk.StringVar()
    entry_password = tk.Entry(
        master=master,
        textvariable=password,
        show='*'
    )
    entry_password.grid(
        row=1, column=1,
        columnspan=2
    )

    def login_callback() -> None:
        nonlocal success
        if success:
            return
        name = username.get()
        pswd = password.get()
        ok, problem = func(
            username=name,
            password=pswd
        )
        if ok:
            success = True
            tk.Label(
                master=master,
                text=f"{mode} Success",
                width=15,
                foreground="green"
            ).grid(
                row=3, column=1,
                columnspan=2
            )
            master.after(
                ms=1000,
                func=success_exit
            )
        else:
            entry_password.delete(0, tk.END)
            if 'username' in problem:
                entry_username.delete(0, tk.END)
            tk.Label(
                master=master,
                text=problem,
                width=15,
                foreground="red",
                wraplength="15i"
            ).grid(
                row=3, column=1,
                columnspan=2
            )
        return

    # `LogIn` / `Register` button
    tk.Button(
        master=master,
        text=mode,
        background="deep sky blue",
        command=login_callback
    ).grid(
        row=2, column=1,
        columnspan=2
    )

    # return Back
    def back_callback() -> None:
        nonlocal user_id, success
        if not success:
            master.destroy()
            user_id = authorization()
        return

    # `Back` button
    tk.Button(
        master=master,
        text="Back",
        command=back_callback
    ).grid(
        row=3, column=0
    )

    master.mainloop()
    return user_id


def authorization() -> int:
    """
    Authorization loop

    :return: User ID
    """
    # create window
    master = tk.Tk()
    master.title("PyProject")
    # get monitor resolution
    w = master.winfo_screenwidth()
    h = master.winfo_screenheight()
    # set window position in center
    master.geometry(f'220x150+{w // 2 - 100}+{h // 2 - 100}')
    # make window non-resizable
    master.resizable(False, False)
    user_id = -1

    def callback(mode: str) -> None:
        nonlocal user_id
        master.destroy()
        user_id = login(mode)
        return

    # LogIn Button
    login_callback = functools.partial(callback, 'LogIn')
    tk.Button(
        master=master,
        text="LogIn",
        width=15,
        font=("Calibri", 14),
        command=login_callback
    ).pack(
        side='top',
        ipadx=5, ipady=5,
        padx=10, pady=10
    )

    # Register Button
    register_callback = functools.partial(callback, 'Register')
    tk.Button(
        master=master,
        text="Register",
        width=15,
        font=("Calibri", 14),
        command=register_callback
    ).pack(
        side='bottom',
        ipadx=5, ipady=5,
        padx=10, pady=10
    )

    master.mainloop()
    return user_id


if __name__ == '__main__':
    print("Run!")
    authorization()
    print("End of run.")
