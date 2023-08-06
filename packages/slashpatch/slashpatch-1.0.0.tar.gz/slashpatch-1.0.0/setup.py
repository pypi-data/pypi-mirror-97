import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slashpatch",
    version="1.0.0",
    author="vcokltfre",
    author_email="vcokltfre@gmail.com",
    description="A command handler/dispatcher webserver for Discord slash commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vcokltfre/slashpatch",
    project_urls={
        "Bug Tracker": "https://github.com/vcokltfre/slashpatch/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)