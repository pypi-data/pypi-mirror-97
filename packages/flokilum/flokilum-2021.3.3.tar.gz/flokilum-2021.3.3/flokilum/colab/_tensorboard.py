def tensorboard(version = "2.4.1"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from tensorboard import __version__ as INFO
        if parse(INFO) < parse(version):
            command("pip install --upgrade tensorboard")
    except:
        command("pip install --upgrade tensorboard")
        from tensorboard import __version__ as INFO

    print(F"{'tensorboard'.rjust(50)} : {INFO}")

    return import_module("tensorboard")
