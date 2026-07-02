import sys
import os
try:
    import dotenv
except ModuleNotFoundError:
    print("python-dotenv module is missing.\nuse: pip install python-dotenv")

def main() -> None:

    print("ORACLE STATUS: Reading the Matrix...\n")

    is_configured: bool = True

    if dotenv.load_dotenv():

        env_values = dotenv.dotenv_values()

        MATRIX_MODE = os.getenv("MATRIX_MODE")
        DATABASE_URL = os.getenv("DATABASE_URL")
        API_KEY = os.getenv("MATRIX_MODE")
        LOG_LEVEL = os.getenv("LOG_LEVEL")
        ZION_ENDPOINT = os.getenv("ZION_ENDPOINT")

        if MATRIX_MODE is None:
            print("MATRIX_MODE is missing.")
            is_configured = False
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

        if is_configured:
            print("Configuration loaded:")
            print(f"Mode: {MATRIX_MODE}")
            print("Database: Connected to local instance")
            print("API Access: Authenticated")
            print(f"Log level: {LOG_LEVEL}")
            print("Zion Network: Online")
        else:
            print("Failed to load configuration. Exiting.")
            sys.exit(1)
        print("\nEnvironment security check:")
        


if __name__ == "__main__":
    main()