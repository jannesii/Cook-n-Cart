# setup.py
from setuptools import setup, find_packages

setup(
    name="CookAndCart",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "cookncart": ["utils/*", "*.qss", "*.json", "*.db"],
    },
    entry_points={
        "console_scripts": [
            "cookandcart=cookandcart.main:main",
        ],
    },
    install_requires=[
        "PySide6",
        # other dependencies
    ],
)
