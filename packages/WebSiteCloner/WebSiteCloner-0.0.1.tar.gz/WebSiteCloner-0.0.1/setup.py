from setuptools import setup, find_packages
import WebSiteCloner

setup(
    name = 'WebSiteCloner',
 
    version = WebSiteCloner.__version__,
    packages = find_packages(),
    install_requires = [],

    author = "Maurice Lambert", 
    author_email = "mauricelambert434@gmail.com",
 
    description = "This package implement a Web Site Cloner and his HTTP server to launch it.",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://github.com/mauricelambert/WebSiteCloner',
 
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
    ],
 
    entry_points = {
        'console_scripts': [
            'WebSiteCloner = WebSiteCloner:cloner',
            'WebClonerServer = WebSiteCloner:server'
        ],
    },
    python_requires='>=3.6',
)