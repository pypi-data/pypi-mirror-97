import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snakeeyes-spaceprius",  # Replace with your own username
    version="0.3.0",
    author="Emily Stringer",
    author_email="emily@spaceprius.com",
    description="A simple python dice library built with regex, currently in alpha",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SpacePrius/SnakeEyes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
