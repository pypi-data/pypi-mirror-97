from setuptools import setup
from prasopes import __version__ #as version


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="prasopes",
    version=__version__,
    author="Jan Zelenka",
    author_email="3yanyanyan@gmail.com",
    description="Thermo/Finnigan .raw file viewer based on rawprasslib",
    long_description=long_description,
    url="https://gitlab.science.ru.nl/jzelenka/prasopes",
    packages=['prasopes'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        ],
    python_requires='>=3.5',
    install_requires=['numpy>=1.13.0',
                      # On Linux distro-packaged Qt/PyQt is preffered
                      'PyQt5;platform_system=="Windows"',
                      'PyQt5-sip;platform_system=="Windows"',
                      'PyQt5;platform_system=="Darwin"',
                      'PyQt5-sip;platform_system=="Darwin"',
                      'matplotlib>=3.0.0',
                      'rawprasslib>=0.0.6',
                      'opentims-bruker-bridge',
                      'opentimspy'],
    extras_require={
        'raw parameters readout': ['rawautoparams>=0.0.3']},
    entry_points={
        'console_scripts': [
            'prasopes = prasopes.__main__:main'
        ],
    }
    )
