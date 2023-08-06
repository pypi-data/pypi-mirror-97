from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='SQLAlchemyBlender',
    version='0.1.52',
    description='Helpers package for SQL-Alchemy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='python library utilities',
    url='https://github.com/kmjbyrne/sqlalchemy-blender',
    author='Keith Byrne',
    author_email='keithmbyrne@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'markdown',
        'twine'
    ],
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    include_package_data=True,
    zip_safe=False
)
