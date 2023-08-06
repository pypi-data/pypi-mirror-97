import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fauna_easy", # Replace with your own username
    version="0.0.1",
    author="DudeBro249",
    description="A convenient wrapper around faunadb-py that abstracts away FQL code for the database service faunadb.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DudeBro249/fauna-easy-py",
    packages=["fauna_easy"],
    include_package_data=True,
    license='Apache License 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires= ["faunadb", "pydantic"]
)
