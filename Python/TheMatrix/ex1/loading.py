print("Loading status: Loading programs...\n")

try:
    from importlib.metadata import version
    import importlib
except ModuleNotFoundError:
    print("importlib is missing.")

try:
    import pandas
    pandas_name = pandas.__name__
    pandas_version = pandas.__version__
except ModuleNotFoundError:
    print("pandas is missing.")

try:
    import numpy
    numpy_version = version("numpy")
    numpy_name = numpy.__name__
except ModuleNotFoundError:
    print("numpy is missing.")

try:
    import matplotlib
    matplotlib_name = matplotlib.__name__
    matplotlib_version = matplotlib.__version__
except ModuleNotFoundError:
    print("matplotlib is missing.")

try:
    import sys
except ModuleNotFoundError:
    # this is a rare case where system .dll and .so files are corrupted
    print("sys is missing or corrupted.")

print("Checking dependencies:")

try:
    print(f"[OK] {pandas_name} ({pandas_version}) - Data manipulation ready")
except NameError:
    print("[KO] - Data manipulation failed")

try:
    print(f"[OK] {numpy_name} ({numpy_version}) - Numerical computation ready")
except NameError:
    print("[KO] - Numerical computation failed")

try:
    print(f"[OK] {matplotlib_name} ({matplotlib_version}) - Visualization ready")
except NameError:
    print("[KO] - Visualization failed")

print("Analyzing matrix data ...")
