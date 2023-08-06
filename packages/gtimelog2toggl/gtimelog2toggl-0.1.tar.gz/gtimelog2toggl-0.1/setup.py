
from setuptools import setup, find_packages


setup(
    packages=find_packages(),
    entry_points={"console_scripts": ["gtimelog2toggl = gtimelog2toggl.cli:main"]},
    include_package_data=True,
    install_requires=[
        "appdirs",
        "click",
        "gtimelog",
        "python-box",
        "ruamel.yaml",
        "TogglPy",
    ]
)
