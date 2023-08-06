from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '1.0.2.2'
DESCRIPTION = 'Es un paquete que tiene como propósito facilitar la comunicación con la API de SPECTRUM a través de ' \
              'Python. '

# Setting up
setup(
    name="spectrum-api-service-bit3",
    version=VERSION,
    author="Mauricio Montoya Medrano",
    author_email="mcubico33@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bitcubico/SpectrumApiServicePy",
    packages=find_packages(),
    install_requires=[
        'lxml>=4.6.2',
        'requests>=2.25.1',
        'setuptools>=53.0.0',
        'log-helper-bit3>=1.2.0'
    ],
    keywords=['python', 'spectrum', 'api', 'arus', 'mcubico'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
    ],
    python_requires='>=3.8',
)
