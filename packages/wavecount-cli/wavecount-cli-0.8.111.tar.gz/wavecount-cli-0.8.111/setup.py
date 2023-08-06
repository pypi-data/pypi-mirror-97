from setuptools import setup, find_packages

from wave_cli import VERSION, PACKAGE_NAME

with open("README.md", "r") as fh:
    long_description = fh.read()

DEPENDENCIES = [
    'requests >= 2.0.0',
    'click >= 7.1.2',
    'halo >= 0.0.30',
    'pyfiglet >= 0.8.post1',
    'pyinquirer >= 1.0.3',
    'pydash >= 4.9.2'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="Wavecount cli",
    author="Navid Ahrary",
    author_email="n.ahrary@avakatan.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="ISC",
    classifiers=[
        "Programming Language :: Python :: 3",
        'Environment :: Console',
        'License :: OSI Approved :: ISC License (ISCL)',
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=['test*', '.vscode']),
    install_requires=DEPENDENCIES,
    python_requires='>=3.6',
    entry_points='''
        [console_scripts]
        wave=wave_cli.wave:main
    ''',
)
