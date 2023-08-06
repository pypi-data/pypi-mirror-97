import setuptools

with open('README.md','r') as fh:
    long_description=fh.read()

setuptools.setup(
    name='mmodule',
    version='21.3.8',
    author='Kevin',
    author_email='mymodule@163.com',
    description='This is a module that includemany useful function.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=None,
    python_requires='>=3.4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
