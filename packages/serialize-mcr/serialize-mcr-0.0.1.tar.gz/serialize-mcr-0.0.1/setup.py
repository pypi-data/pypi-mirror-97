import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='serialize-mcr',
    version='0.0.1',
    author='Andrew Ray',
    author_email='rayam@iu.edu',
    description='Creating a serializer for data structures',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/millcityrunner/serialize-mcr',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        'flask-sqlalchemy',
        'sqlalchemy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
