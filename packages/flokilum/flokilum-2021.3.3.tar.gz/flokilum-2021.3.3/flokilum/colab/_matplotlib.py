def matplotlib(version = "3.3.4", seaborn_version = "0.11.1"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from matplotlib import __version__ as INFO
        if parse(INFO) < parse(version):
            command("pip install --upgrade matplotlib")
    except:
        command("pip install --upgrade matplotlib")
        from matplotlib import __version__ as INFO

    try:
        from seaborn import __version__ as INFO1
        if parse(INFO1) < parse(seaborn_version):
            command("pip install --upgrade seaborn")
    except:
        command("pip install --upgrade seaborn")
        from seaborn import __version__ as INFO1

    print(F"{'matplotlib'.rjust(50)} : {INFO}")
    print(F"{'seaborn'.rjust(50)} : {INFO1}")

    return (
        import_module("matplotlib"),
        import_module("matplotlib.pyplot"),
        import_module("seaborn")
    )
