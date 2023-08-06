from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name = "flokilum",
    version = "2021.03.03",
    description = "google colab helper",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/pypa/sampleproject",
    author = "flokilum",
    author_email = "flokilum@example.com",
    license = "MIT",

    classifiers = [
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
    ],

    package_dir={"flokilum/": ""},

    packages = [
        "flokilum",
        "flokilum/colab",
    ],

    python_requires = ">=3.6",
)
