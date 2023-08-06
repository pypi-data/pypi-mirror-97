from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name="gopublic",
    version='0.0.1',
    description="Go-publish CLI",
    author="Mateo Boudet",
    author_email="mateo.boudet@inrae.fr",
    url="https://github.com/mboudet/gopublish_cli",
    install_requires=requires,
    packages=find_packages(),
    license='MIT',
    platforms="Posix; MacOS X; Windows",
    entry_points='''
        [console_scripts]
        gopublic=gopublic.cli:gopublic
    ''',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3.7",
    ]
)
