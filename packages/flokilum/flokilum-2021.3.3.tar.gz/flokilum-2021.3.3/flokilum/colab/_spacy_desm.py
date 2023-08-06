def spacy_desm(version = "3.0.0"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from de_core_news_sm import __version__ as INFO
        if parse(INFO) < parse(version):
            command("python -m spacy download de_core_news_sm")
    except:
        command("python -m spacy download de_core_news_sm")
        from de_core_news_sm import __version__ as INFO

    print(F"{'spacy_desm = de_core_news_sm'.rjust(50)} : {INFO}")

    return import_module("de_core_news_sm")
