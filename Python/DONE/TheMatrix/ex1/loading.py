def main() -> None:
    print("LOADING STATUS: Loading programs...\n")

    try:
        from importlib.metadata import version
    except ImportError:
        print("importlib is missing.")

    try:
        import numpy

        numpy_name: str = numpy.__name__
        numpy_version: str = version("numpy")
    except ImportError:
        print("numpy is missing.")

    try:
        import pandas

        pandas_name: str = pandas.__name__
        pandas_version: str = pandas.__version__
    except ImportError as e:
        if "numpy" in str(e).lower():
            print("pandas is installed, but it crashed because numpy is missing.")
        else:
            print("pandas is completely missing.")

    try:
        import matplotlib.pyplot

        matplotlib_name: str = matplotlib.__name__
        matplotlib_version: str = matplotlib.__version__
    except ImportError as e:
        if "numpy" in str(e).lower():
            print("matplotlib is installed, but it crashed because numpy is missing.")
        else:
            print("matplotlib is completely missing.")

    packages_loaded: bool = True
    print("Checking dependencies:")
    try:
        print(f"[OK] {pandas_name} ({pandas_version}) - Data manipulation ready")
    except NameError:
        packages_loaded = False
        print("[KO] - Data manipulation failed")

    try:
        print(f"[OK] {numpy_name} ({numpy_version}) - Numerical computation ready")
    except NameError:
        packages_loaded = False
        print("[KO] - Numerical computation failed")

    try:
        print(f"[OK] {matplotlib_name} ({matplotlib_version}) - Visualization ready")
    except NameError:
        packages_loaded = False
        print("[KO] - Visualization failed")

    if packages_loaded:
        print("\nAnalyzing Matrix data...")
        print("Processing 1000 data points...")

        t = numpy.linspace(0, 2 * numpy.pi, 1000)
        xpoints = numpy.cos(t) / (1 + numpy.sin(t) ** 2)
        ypoints = (numpy.sin(t) * numpy.cos(t)) / (1 + numpy.sin(t) ** 2)

        print("Generating visualization...")
        matplotlib.pyplot.plot(xpoints, ypoints, color="green")
        matplotlib.pyplot.axis("off")
        matplotlib.pyplot.savefig("matrix_analysis.png")

        print("Analysis complete!")
        print("Results saved to: matrix_analysis.png")
    else:
        print("Packages failed to load.")


if __name__ == "__main__":
    main()
