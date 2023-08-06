import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="spampost",
    version="1.0.4",
    description="Check blog's spam post",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/narupo/spampost",
    author="narupo",
    author_email="narupo.glab@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["spampost"],
    include_package_data=True,
    install_requires=[
        "BeautifulSoup4",
        "soupsieve",
        "janome",
    ],
    entry_points={
        "console_scripts": [
            "spampost=spampost.__main__:main",
        ]
    },
)