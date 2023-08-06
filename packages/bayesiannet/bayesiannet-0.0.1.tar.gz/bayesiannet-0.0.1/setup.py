import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bayesiannet", 
    version="0.0.1",
    author="Zohim Chandani",
    author_email="zohim.chandani@hotmail.co.uk",
    description="Bayesian Network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zohimchandani/CQCtest",
    project_urls={ "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)