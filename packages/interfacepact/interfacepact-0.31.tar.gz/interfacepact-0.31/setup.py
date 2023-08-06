import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="interfacepact",
    version="0.31",
    author="jaygeli",
    author_email="348447053@qq.com",
    description="interface pact verify",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crazymonkey/PactVerify_demo",
    packages=setuptools.find_packages(),
    install_requires=['six'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)