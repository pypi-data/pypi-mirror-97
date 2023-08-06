def spacy_ensm(version = "3.0.0"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from en_core_web_sm import __version__ as INFO
        if parse(INFO) < parse(version):
            command("python -m spacy download en_core_web_sm")
    except:
        command("python -m spacy download en_core_web_sm")
        from en_core_web_sm import __version__ as INFO

    print(F"{'spacy_ensm = en_core_web_sm'.rjust(50)} : {INFO}")

    return import_module("en_core_web_sm")
