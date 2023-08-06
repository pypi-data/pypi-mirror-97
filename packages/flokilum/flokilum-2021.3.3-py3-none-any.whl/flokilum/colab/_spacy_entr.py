def spacy_entr(version = "3.0.0"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from en_core_web_trf import __version__ as INFO
        if parse(INFO) < parse(version):
            command("python -m spacy download en_core_web_trf")
    except:
        command("python -m spacy download en_core_web_trf")
        from en_core_web_trf import __version__ as INFO

    print(F"{'spacy_entr = en_core_web_trf'.rjust(50)} : {INFO}")

    return import_module("en_core_web_trf")
