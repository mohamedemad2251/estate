from setuptools import setup, find_packages

setup(
    name="estate",
    version="1.0.0",
    author="Mohamed Emad",
    description="A real estate management module for Odoo",
    license="AGPL-3",
    include_package_data=True,  # Ensures non-Python files are included
    package_data={
        "estate": ["**/*"],  # Explicitly includes all files inside estate/
    },
    install_requires=[],
)

