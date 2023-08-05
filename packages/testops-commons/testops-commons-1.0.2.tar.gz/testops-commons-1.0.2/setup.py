import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

REQUIRES=[
    "requests",
    "testops-api",
    "jsonpickle"
]

setuptools.setup(
    name="testops-commons",
    version="1.0.2",
    author="Katalon, LLC. (https://www.katalon.com)",
    author_email="info@katalon.io",
    description="TestOps Commons Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/katalon-studio/testops-commons-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
    ],
    keywords=["Katalon", "TestOps"],
    python_requires='>=3.6',
    install_requires=REQUIRES
)
