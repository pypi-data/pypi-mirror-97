from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = "teachmedijkstra", 
    version = "0.1.0",
    author = "Milan Petrík",
    author_email = "milan.petrik@protonmail.com",
    description = "Demonstration of the Dijkstra algorithm for educational purposes",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "GPLv3",
    url = "https://gitlab.com/petrikm/teachmedijkstra",
    packages = find_packages(),
    install_requires = [],
    python_requires = ">=3.6",
    keywords = ["Graph", "Finding shortest path"],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Intended Audience :: Education",
    ]
)
