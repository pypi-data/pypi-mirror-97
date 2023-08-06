from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name="cian",
    version="0.1.1",
    
    author="Oleg Yurchik",
    author_email="oleg.yurchik@protonmail.com",
    url="https://github.com/OlegYurchik/cian",
    
    description="Sync/async library for searching offers on Cian",
    long_description=open(join(dirname(__file__), "README.md")).read(),
    long_description_content_type="text/markdown",
    
    packages=find_packages(),
    test_suite="cian.tests",

    install_requires=[
        "aiohttp",
        "yarl",
    ],
    tests_require=[
        "pytest",
    ],
)
