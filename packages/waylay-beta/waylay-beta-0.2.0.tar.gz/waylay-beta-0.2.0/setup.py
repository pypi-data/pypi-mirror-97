"""waylay-beta build configuration"""
from setuptools import setup, find_namespace_packages
import versioneer

with open("doc/dist.README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='waylay-beta',
    description='beta release of the Waylay Python SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url='https://docs-io.waylay.io/#/api/sdk/python',
    author='Waylay',
    author_email='info@waylay.io',
    license='ISC',
    license_file='LICENSE.txt',
    packages=find_namespace_packages(),
    package_data={"waylay": ["py.typed"]},
    include_package_data=True,
    install_requires=[
        'httpx',
        'simple-rest-client',
        'appdirs',
        'python-jose',
        'pandas',
        'isodate',
        'joblib',
        'tqdm',  # progres bar
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'pytest-mock',
            'mock',
            'pylint',
            'pycodestyle',
            'pydocstyle',
            'autopep8',
            'mypy',
            'typing-inspect',
            'sklearn',
            'pdoc',
        ],
        ':python_version == "3.6"': [
            'python-dateutil',
            'dataclasses',
            'typing_extensions'
        ],
        ':python_version == "3.7"': [
            'typing_extensions'
        ],
    },
    setup_requires=[
        'setuptools-pep8'
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "waylaycli = waylay.cli.waylaycli:main"
        ],
        "waylay_services": [
            "beta = waylay.service:SERVICES"
        ]
    }
)
