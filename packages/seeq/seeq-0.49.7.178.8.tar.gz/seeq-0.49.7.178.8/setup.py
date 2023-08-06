import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seeq",
    version="0.49.07.178.8",
    author="Seeq Corporation",
    author_email="support@seeq.com",
    description="The Seeq SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.seeq.com",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        # These requirements are for seeq.sdk and should match target/python/requirements.txt
        'certifi >= 14.05.14',
        'six >= 1.10',
        'urllib3 >= 1.15.1',
        'requests >= 2.21.0',
        'cryptography >= 3.2',
        # cryptography 3.3 requires pyOpenSSL >= 19.1.0
        'pyOpenSSL >= 19.1.0',

        # These additional requirements are for seeq.spy
        'ipython >= 7.6.1',
        'matplotlib >= 3.1.1',
        'numpy >= 1.16.4',
        'pandas >= 1.0.0',
        'beautifulsoup4 >= 4.8.0',
        'Deprecated >= 1.2.6',
        'Mako >= 1.1.0',
        'ipywidgets >= 7.5.1',
        'tzlocal >= 2.0.0',
        'dataclasses >= 0.7; python_version == "3.6"'        # This is a polyfill for dataclasses in Python 3.6.
                                                             # They're standard in Python 3.7.
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
)
