import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='midas-atoolkit',
    version='0.0.1',
    author='Luciano Ambrosini',
    author_email='luciano.ambrosini@outlook.com',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/lucianoambrosini/Ambrosinus-Toolkit',
    project_urls = {
        "Bug Tracker": "https://github.com/lucianoambrosini/Ambrosinus-Toolkit/midas-atoolkit"
    },
    license='MIT',
    packages=['midas-atoolkit'],
    install_requires=['requests'],
)