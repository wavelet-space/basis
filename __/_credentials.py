class Credentials:
    """
    e.g PostgreSQL credentials.
    """

    def __init__(self, user: str, host: str, password: str, dbname: str):
        self._credentials = (
            f"dbname={dbname} host={host} password={password} user={user}"
        )

    def __call__(self) -> str:
        return self._credentials
