import setuptools
from pathlib import Path
import os

maindir = Path(__file__).resolve().parent.parent
readme = os.path.join(maindir,"README.md")

with open(readme, "r", encoding="utf-8") as fh:
    long_description = fh.read()
    print(long_description)

setuptools.setup(
    name="EchidnaLib", # Replace with your own username
    version="0.0.1",
    author="IdleEchidna",
    author_email="",
    description="A modular discord bot package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IdleEchidna/EchidnaLib",
    project_urls={
        "Bug Tracker": "https://github.com/IdleEchidna/EchidnaLib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
)
