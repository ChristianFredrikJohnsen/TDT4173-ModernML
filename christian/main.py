import sys

def main():
    assert sys.version.split()[0] == "3.14.0", f"If you're using the uv environment correctly, your python version should be 3.14.0. You're using {sys.version.split()[0]}"
    print(f"You're using the correct Python version (3.14.0)")
    print(f"Detailed version info: {sys.version}")

if __name__ == "__main__":
    main()
