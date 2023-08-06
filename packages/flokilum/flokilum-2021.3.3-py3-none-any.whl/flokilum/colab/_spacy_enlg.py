def spacy_enlg(version = "3.0.0"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from en_core_web_lg import __version__ as INFO
        if parse(INFO) < parse(version):
            command("python -m spacy download en_core_web_lg")
    except:
        command("python -m spacy download en_core_web_lg")
        from en_core_web_lg import __version__ as INFO

    print(F"{'spacy_enlg = en_core_web_lg'.rjust(50)} : {INFO}")

    return import_module("en_core_web_lg")
