from setuptools import setup, find_packages
import PyEmailTools

setup(
    name = 'PyEmailTools',
 
    version = PyEmailTools.__version__,
    packages = find_packages(),

    author = "Maurice Lambert", 
    author_email = "mauricelambert434@gmail.com",
 
    description = "This package implement tools for email analysis and email forgering.",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://github.com/mauricelambert/PyEmailTools',
 
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Security"
    ],
 
    entry_points = {
        'console_scripts': [
            'EmailForgering = PyEmailTools:forger',
            'EmailAnalysis = PyEmailTools:analysis'
        ],
    },
    python_requires='>=3.6',
)