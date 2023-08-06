class MDX():

    def __init__(self, directory):

        from pathlib import Path
        from shutil import rmtree

        dir = Path(directory)
        mdx = dir / "index.mdx"

        if dir.is_dir(): rmtree(dir)
        dir.mkdir(parents=True)

        self.dir = dir
        self.mdx = mdx
        self.idx = 1 ## for figures

    def text(self, text):

        text = text.strip()
        text = F"{text}\n\n"

        with self.mdx.open("a") as file:
            file.write(text)

    def code(self, code):

        from contextlib import redirect_stdout
        from inspect import getsource
        from io import StringIO
        from re import sub

        source = getsource(code)
        source = source.replace("\n    ", "\n")
        source = sub("^def.*\n", "", source)

        text = F"``` python\n{source}\n```"
        self.text(text)

        ## run code and capture output
        output = StringIO()

        with redirect_stdout(output):
            code()

        text = output.getvalue()

        text = text.strip()

        if text != "":
            print(text)
            text = F"```\nOUTPUT:\n\n{text}\n```"
            self.text(text)

    def pict(self, pict):

        from pathlib import Path

        pict = Path(pict)

        name = F"image-{self.idx}.png"

        target = self.dir / name
        pict.rename(target)

        text = F"![]({name})"
        self.text(text)

        self.idx += 1
