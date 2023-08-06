import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(

    name="hthPkg",

    version="0.0.4",

    install_requires=[
            "Django==3.0.3",
            "configparser==4.0.2",
            "django-cors-headers==3.2.1",
            "djangorestframework==3.11.0",
            "pycryptodome==3.9.7",
            "mysqlclient==1.4.6",
            "sqlalchemy==1.3.13",
            "pdfminer.six==20191110",
            "requests==2.22.0",
            "six==1.13.0",
            "xlrd==1.2.0",
            "XlsxWriter==1.2.3",
            "pymysql==0.9.3",
            "lxml==4.4.2",
            "pyhwp==0.1b12",
            "BeautifulSoup4==4.8.2"
        ],

    author="Example Author",

    author_email="author@example.com",

    description="A small example package",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/pypa/sampleproject",

    packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],
    python_requires='>=3.6',

)
