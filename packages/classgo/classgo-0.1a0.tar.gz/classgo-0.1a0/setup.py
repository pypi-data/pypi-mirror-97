from setuptools import setup
from setuptools import find_packages

setup(
    package=find_packages(),
    include_packages_data=True,
    install_requires=[
        "click"],
    entry_points="""
        [console_scripts]
        class=class_go.scripts:cli
    """
)