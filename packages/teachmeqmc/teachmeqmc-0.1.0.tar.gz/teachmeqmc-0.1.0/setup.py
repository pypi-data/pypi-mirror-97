from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = "teachmeqmc", 
    version = "0.1.0",
    author = "Milan Petrík",
    author_email = "milan.petrik@protonmail.com",
    description = "Demonstration of the Quine-McCluskey algorithm for educational purposes",
#    long_description = "Produces a LaTeX code with detailed description of the performing of the Quine-McCluskey algorithm.",
#    long_description = open('README.md').read(),
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "GPLv3",
    url = "https://gitlab.com/petrikm/teachmeqmc",
#    download_url = 'https://gitlab.com/petrikm/teachmeqmc/...",
    packages = find_packages(),
    install_requires = [], # additional packages that need to be installed along with this package
    python_requires = ">=3.6",
    keywords = ["Quine-McCluskey algorithm", "Minimal Disjunctive Normal Form", "Boolean Function", "Hardware Design"],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Intended Audience :: Education",
    ]
)
