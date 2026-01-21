def getenv(key: str) -> str:
    from os import getenv as g_e
    from dotenv import load_dotenv

    load_dotenv()

    return g_e(key)