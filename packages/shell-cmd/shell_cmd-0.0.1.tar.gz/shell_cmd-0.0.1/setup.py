import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shell_cmd",
    version="0.0.1",
    author="Arturo Fernandez",
    description="Execute shell commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Code": "https://github.com/bsnux/shell-cmd",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.2",
)