def torchvision(version = "0.9.0"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from torchvision import __version__ as INFO
        if parse(INFO) < parse(version):
            command("pip install --upgrade torchvision")
    except:
        command("pip install --upgrade torchvision")
        from torchvision import __version__ as INFO

    print(F"{'torchvision'.rjust(50)} : {INFO}")

    return import_module("torchvision")
