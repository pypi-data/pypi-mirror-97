import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="mxmul",
    version="0.1.0",
    author="suiyi",
    license = 'License',
    author_email="h2838443896@163.com",
    description="new learner",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://pypi.org/",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)