def numpy(version = "1.20.1", einops_version="0.3"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from numpy import __version__ as INFO
        if parse(INFO) < parse(version):
            command("pip install --upgrade numpy")
    except:
        command("pip install --upgrade numpy")
        from numpy import __version__ as INFO

    try:
        from einops import __version__ as INFO1
        if parse(INFO1) < parse(einops_version):
            command("pip install --upgrade einops")
    except:
        command("pip install --upgrade einops")
        from einops import __version__ as INFO1

    print(F"{'numpy, einops'.rjust(50)} : {INFO}, {INFO1}")

    return import_module("numpy")
