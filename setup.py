from setuptools import setup

setup(
    name="budbt",
    version="0.1.4",
    author="David Gasquez",
    author_email="davidgasquez@buffer.com",
    install_requires=["stacklogging", "dbt"],
    license="MIT license",
    entry_points={"console_scripts": ["budbt=cli:main"]},
)
