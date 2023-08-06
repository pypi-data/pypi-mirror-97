# pylint: disable=invalid-name
import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="drvn.installer",
    author="Hallgrimur David Egilsson",
    author_email="hallgrimur1471@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hallgrimur1471/drvn_installer",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="src"),
    package_data={"": ["*"]},
    entry_points={
        "console_scripts": [
            "drvn_installer = drvn.installer._script:main"
        ]
    },
    install_requires=[],
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
)
