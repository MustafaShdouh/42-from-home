#!/usr/bin/env python3
def secure_archive(filename: str, action: str = 'r',
                   content: str = '') -> tuple[bool, str]:
    try:
        if action == 'w':
            with open(filename, 'w') as file:
                file.write(content)
            return (True, 'Content successfully written to file')
        else:
            with open(filename, 'r') as file:
                data = file.read()
            return (True, data)
    except Exception as e:
        return (False, str(e))


def main() -> None:
    print("=== Cyber Archives Security ===")
    print("\nUsing 'secure_archive' to read from a nonexistent file:")
    success, result = secure_archive('/not/existing/file')
    print(f"({success}, \"{result}\")")
    print("\nUsing 'secure_archive' to read from an inaccessible file:")
    success, result = secure_archive('/etc/master.passwd')
    print(f"({success}, \"{result}\")")
    print("\nUsing 'secure_archive' to read from a regular file:")
    success, result = secure_archive('ancient_fragment.txt')
    print(f"({success}, '{repr(result)[1:-1]}')")
    print("\nUsing 'secure_archive' to write previous content to a new file:")
    success, result = secure_archive('new_fragment.txt', 'w', result)
    print(f"({success}, '{result}')")


if __name__ == "__main__":
    main()
