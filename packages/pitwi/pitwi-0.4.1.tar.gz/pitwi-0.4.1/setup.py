import setuptools


with open("README.md", "r", encoding='utf-8') as fichier:
    long_description = fichier.read()


setuptools.setup(
    name = "pitwi",
    version = "0.4.1",
    author = "Asurix",
    author_email = "asurix@outlook.fr",
    description = "User interface for terminal.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/4surix/pitwi",
    packages = setuptools.find_packages(),
    keywords = 'terminal gui console user interface',
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3 :: Only',
        'Natural Language :: French',
    ],
    python_requires = '>=3, <4',
)