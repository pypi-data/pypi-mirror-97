from setuptools import setup, find_packages

setup(
    name="keystorage",
    version="0.2.1.dev1",
    package=find_packages(),
    include_packages_data=True,
    install_requires=[
        "click", "pycrypto"
    ],
    entry_points="""
        [console_scripts]
        keys=keystorage.scripts:cli
    """
)