from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt", "r") as req:
        content = req.read()
        requirements = content.split("\n")

    return requirements


setup(
    name="scdlp",
    version="0.1",
    author="jayvishaalj",
    author_email="jayvishaalj.01@gmail.com",
    url="https://github.com/jayvishaalj/scdlp",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points="""
        [console_scripts]
        scdlp=scdlp.cli:cli
    """,
)