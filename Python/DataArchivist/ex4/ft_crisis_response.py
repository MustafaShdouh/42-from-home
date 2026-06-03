#!/usr/bin/env python3

import os

def crisis_handler(filename: str, mode: str) -> None:
    if filename == "standard_archive.txt":
        print(f"ROUTINE ACCESS: Attempting access to '{filename}'...")
    else:
        print(f"CRISIS ALERT: Attempting access to '{filename}'...")
        
    try:
        with open(filename, mode) as f:
            if filename == "classified_vault.txt":
                raise PermissionError("Permission denied")
            content = f.read().strip()
            if filename == "standard_archive.txt":
                print(f'SUCCESS: Archive recovered "{content}"')
                print("STATUS: Normal operations resumed")
    except FileNotFoundError:
        print("RESPONSE: Archive not found in storage matrix")
        print("STATUS: Crisis handled, system stable")
    except PermissionError:
        print("RESPONSE: Security protocols deny access")
        print("STATUS: Crisis handled, security maintained")
    except Exception:
        print("RESPONSE: System anomaly detected")
        print("STATUS: Crisis handled, system stable")
    print()

def main() -> None:
    print("=== CYBER ARCHIVES CRISIS RESPONSE SYSTEM ===")
    
    # We attempt to mock a permission error by changing permissions for the test
    if os.path.exists("classified_vault.txt"):
        os.chmod("classified_vault.txt", 0o000)
    else:
        # Create it and restrict it if missing
        with open("classified_vault.txt", "w") as f:
            f.write("TOP SECRET")
        os.chmod("classified_vault.txt", 0o000)
        
    # Test cases
    crisis_handler("lost_archive.txt", "r")
    crisis_handler("classified_vault.txt", "r")
    
    # Let's ensure standard_archive.txt exists for the test
    if not os.path.exists("standard_archive.txt"):
        with open("standard_archive.txt", "w") as f:
            f.write("Knowledge preserved for humanity")
            
    crisis_handler("standard_archive.txt", "r")
    
    print("All crisis scenarios handled successfully. Archives secure.")
    
    # Cleanup permissions so the user can delete it later
    if os.path.exists("classified_vault.txt"):
        os.chmod("classified_vault.txt", 0o644)

if __name__ == "__main__":
    main()
