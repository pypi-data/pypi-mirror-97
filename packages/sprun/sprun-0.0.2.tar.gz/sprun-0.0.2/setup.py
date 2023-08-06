import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sprun",
    version="0.0.2",
    author="Harald Achitz",
    author_email="harald.achitz@gmail.com",
    description="subprocess run, simply execute a list of commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/a4z/sprun",
    project_urls={
        "Bug Tracker": "https://gitlab.com/a4z/sprun/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
