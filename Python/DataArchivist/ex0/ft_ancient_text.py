#!/usr/bin/env python3

def main() -> None:
    try:
        file = open("ancient_fragment.txt", "r")
        print("=== CYBER ARCHIVES DATA RECOVERY SYSTEM ===")
        print("Accessing Storage Vault: ancient_fragment.txt")
        print("Connection established...")
        print("RECOVERED DATA:")
        content = file.read()
        print(content.strip())
        print("Data recovery complete. Storage unit disconnected.")
        file.close()
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")

if __name__ == "__main__":
    main()
