import os
try:
    import dotenv
    dotenv.load_dotenv()
except ModuleNotFoundError:
    print("Python-dotenv module is missing.\nUse: pip install python-dotenv\n")


def get_env_var(key: str, default: str | None = None) -> str | None:
    value: str | None = os.getenv(key)
    if value is None or value.strip() == "":
        return default
    return value


def main() -> None:

    print("ORACLE STATUS: Reading the Matrix...\n")

    is_configured: bool = True
    is_mode: bool = True

    MATRIX_MODE: str | None = get_env_var("MATRIX_MODE")
    DATABASE_URL: str | None = get_env_var("DATABASE_URL")
    API_KEY: str | None = get_env_var("API_KEY")
    LOG_LEVEL: str | None = get_env_var("LOG_LEVEL")
    ZION_ENDPOINT: str | None = get_env_var("ZION_ENDPOINT")

    if MATRIX_MODE is None:
        print("MATRIX_MODE is missing.")
        is_configured = False
        is_mode = False
    if DATABASE_URL is None:
        print("DATABASE_URL is missing.")
        is_configured = False
    if API_KEY is None:
        print("API_KEY is missing.")
        is_configured = False
    if LOG_LEVEL is None:
        print("LOG_LEVEL is missing.")
        is_configured = False
    if ZION_ENDPOINT is None:
        print("ZION_ENDPOINT is missing.")
        is_configured = False

    if is_configured and MATRIX_MODE is not None and LOG_LEVEL is not None:
        if MATRIX_MODE.lower().capitalize() == "Production":
            print("Configuration loaded:")
            print(f"Mode: {MATRIX_MODE.lower().capitalize()}")
            print("Database: Connected to local instance")
            print("API Access: Authenticated")
            print(f"Log level: {LOG_LEVEL.upper()}")
            print("Zion Network: Online")
        elif MATRIX_MODE.lower().capitalize() == "Development":
            print("Configuration loaded:")
            print(f"Mode: {MATRIX_MODE.lower().capitalize()}")
            print(f"Database: {DATABASE_URL}")
            print(f"API key: {API_KEY}")
            print(f"Log level: {LOG_LEVEL.upper()}")
            print(f"Zion Network: {ZION_ENDPOINT}")
        else:
            print("Enter a valid MATRIX_MODE.")
            is_configured = False
    else:
        print("Failed to read the Matrix because there "
              "are no env variables or dotenv module is missing.")

    print("\nEnvironment security check:")

    if is_configured:
        print("[OK] No hardcoded secrets detected")
        print("[OK] .env file properly configured")
    else:
        print("[KO] No hardcoded secrets detected")
        print("[KO] .env file properly configured")

    if MATRIX_MODE is not None and \
       MATRIX_MODE.lower().capitalize() == "Production" and is_mode:
        print("[OK] Production overrides available")
    else:
        print("[KO] Production overrides available")


if __name__ == "__main__":
    main()
