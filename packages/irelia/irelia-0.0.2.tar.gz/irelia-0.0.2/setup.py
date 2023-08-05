import pathlib
from irelia import __version__
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent.resolve()

README = (HERE / "README.md").read_text()

description = "A lolesports api wrapper"
keywords = "api, lol, league of legends, lolesports, esports, wrapper"


setup(
    name="irelia",
    version=__version__,
    description=description,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/bgraver/Irelia",
    author="Brandon Graver",
    author_email="graver.brandon@gmail.com",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords=keywords,
    packages=find_packages(where="irelia"),
    python_requires=">=3",
    install_requires=["requests"],
    project_urls = {
        "Source": "https://github.com/bgraver/Irelia",
        "Original API": "https://vickz84259.github.io/lolesports-api-docs/"
    }
)
