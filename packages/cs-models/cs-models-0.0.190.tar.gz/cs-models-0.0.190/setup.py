import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


INSTALL_REQUIRES = [
    "marshmallow==2.10.5",
    "PyMySQL==0.9.3",
    "python-dateutil==2.8.0",
    "pytz==2019.1",
    "SQLAlchemy==1.2.15",
    "boto3==1.14.0",
    "botocore==1.17.63",
    "s3transfer==0.3.4",
    "six==1.12.0",
    "urllib3==1.24.2",
    "dnspython==1.16.0",
    "pymongo==3.8.0",
    "psycopg2-binary==2.8.4",
]

if __name__ == "__main__":
    setuptools.setup(
        name="cs-models",
        version="0.0.190",
        author="Harsh Verma",
        author_email="harsh@capitolscience.com",
        description="MySQL db models",
        # long_description=long_description,
        # long_description_content_type='text/markdown',
        url="https://github.com/ezpz76/cs-models",
        packages=setuptools.find_packages(where="src"),
        package_dir={"": "src"},
        classifiers=["Programming Language :: Python :: 3",],
        install_requires=INSTALL_REQUIRES,
        python_requires="~=3.6",
    )
