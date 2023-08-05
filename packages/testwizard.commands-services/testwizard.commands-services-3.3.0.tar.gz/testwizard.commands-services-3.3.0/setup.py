import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testwizard.commands-services",
    version="3.3.0",
    author="Eurofins Digital Testing - Belgium",
    author_email="support-be@eurofins.com",
    description="Testwizard Services commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['testwizard.commands_services'],
    install_requires=[
        'testwizard.commands-core==3.3.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
    ],
)






