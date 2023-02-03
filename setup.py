from setuptools import setup, find_packages
import os

version = os.getenv('PACKAGE_VERSION')

def get_requirements():
    lines = []
    for line in open("requirements.txt"):
        line = line.strip()
        if not line.startswith(('-', '#')):
            lines.append(line)
    return lines


requirements = get_requirements()

setup(
    # Application name:
    name="pd-ui-backend",

    # Version number (initial):
    version=version,

    # Application author details:
    author="Abhay Kumar",
    author_email="abhay.kumar2@quintiles.com",

    # Packages
    packages=find_packages(),

	# Packages
    data_files=[('', ['requirements.txt']),
                ],
	include_package_data=True,

    # Details
    url="http://ca2spdml01q:8000/docs",

    license="Usage restricted to IQVIA employees.",
    description="Backend light-weight api for various operations.",

    long_description=open("README.md").read(),

    # Dependent packages (distributions)
    install_requires=requirements,

<<<<<<< HEAD
	python_requires=">=3.7.3",
=======
	python_requires=">=3.7",
>>>>>>> 8b95e97247bfd69d4ee069e419096860e93f957b

	entry_points={
        'console_scripts': [
            'pd-ui-backend = main:cli',
        ]
    }

)
