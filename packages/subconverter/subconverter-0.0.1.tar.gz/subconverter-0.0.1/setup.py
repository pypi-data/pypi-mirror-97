import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="subconverter", # Replace with your own username
    version="0.0.1",
    author="Dharmveer Baloda",
    author_email="dharmvrbaloda836@gmail.com",
    description="Convert content into different subtitle formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/baloda/subconverter",
    project_urls={
        "Bug Tracker": "https://github.com/baloda/subconverter/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)