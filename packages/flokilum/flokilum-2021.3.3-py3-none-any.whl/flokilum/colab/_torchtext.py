def torchtext(version = "0.9.0"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from torchtext import __version__ as INFO
        if parse(INFO) < parse(version):
            command("pip install --upgrade torchtext")
    except:
        command("pip install --upgrade torchtext")
        from torchtext import __version__ as INFO

    print(F"{'torchtext'.rjust(50)} : {INFO}")

    return import_module("torchtext")
