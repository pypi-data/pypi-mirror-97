import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JackLin07", # Replace with your own username
    version="0.0.1",
    author="JackLin07",
    author_email="author@example.com",
    description="A small build tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JackLin00/hasaki",
    project_urls={
        "Bug Tracker": "https://github.com/JackLin00/hasaki",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)