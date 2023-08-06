def spacy(version = "3.0.3"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from spacy import __version__ as INFO
        if parse(INFO) < parse(version):
            command("pip install --upgrade spacy")
    except:
        command("pip install --upgrade spacy")
        from spacy import __version__ as INFO

    print(F"{'spacy'.rjust(50)} : {INFO}")

    return import_module("spacy")
