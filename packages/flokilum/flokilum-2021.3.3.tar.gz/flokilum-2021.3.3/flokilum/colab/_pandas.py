def pandas(version = "1.2.3"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from pandas import __version__ as INFO
        if parse(INFO) < parse(version):
            command("pip install --upgrade pandas")
    except:
        command("pip install --upgrade pandas")
        from pandas import __version__ as INFO

    print(F"{'pandas'.rjust(50)} : {INFO}")

    return import_module("pandas")
