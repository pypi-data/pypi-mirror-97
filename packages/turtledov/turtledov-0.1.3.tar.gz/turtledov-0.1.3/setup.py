import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="turtledov",
    version="0.1.3",
    author="Hirusha Pramuditha",
    author_email="hirushapramuditha26@gmail.com",
    description="Learn Python the creative way",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HirushaPramuditha/turtledov",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
