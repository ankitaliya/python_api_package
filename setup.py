import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="museum_api_convert_files",
    version="0.1.1",
    author="Ankita Liya",
    author_email="ankitaliya321@gmail.com",
    description="A package for generating API data reports in different formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ankitaliya/package_python",
    project_urls={
        "Bug Tracker": "https://github.com/ankitaliya/package_python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=['pandas', 'requests', 'pdfkit', 'lxml', 'openpyxl'],
    python_requires=">=3.6",
)
