from src.authorization.database import UserDB


def authorization(kind: str = "") -> int:
    """
    Authorization loop

    :kind: "R" - Register, "L" - LogIn
    :return: User ID
    """
    kind = kind.upper()
    while kind not in ('R', 'L'):
        kind = input("[R]egister or [L]ogIn ? ").upper()

    db = UserDB()
    func = db.check_login if kind == 'L' else db.add

    while True:
        username = input("username: ")
        password = input("password: ")
        ok, problem = func(username, password)
        if ok:
            print(f"Welcome, {username}!")
            return db.get_user_id(username, password)
        else:
            print(problem)
