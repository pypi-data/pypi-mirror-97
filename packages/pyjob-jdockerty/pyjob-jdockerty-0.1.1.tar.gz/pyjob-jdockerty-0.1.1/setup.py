from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="pyjob-jdockerty",
    author="jdockerty",
    description="Job searching through code, interaction to the Reed API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jdockerty/pyjob",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'loguru',
        'pyjob',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points="""
    [console_scripts]
    pyjob=pyjob.cli.main:cli
    """
)