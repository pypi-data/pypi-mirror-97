import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ZKBattleship",
    version="1.0.0",
    author="Gavin Pai",
    author_email="gavinpai@hotmail.com",
    description="Battleship with cryptographic protections and a zero-knowledge framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SteelShredder/ZKBattleship",
    project_urls={
        "Bug Tracker": "https://github.com/SteelShredder/ZKBattleship/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Natural Language :: English",
        "Topic :: Security :: Cryptography",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)
