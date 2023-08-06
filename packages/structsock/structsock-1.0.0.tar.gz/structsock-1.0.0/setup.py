from setuptools import setup

with open('README.md') as f:
    long_desc = f.read()

setup(
    name='structsock',
    version='1.0.0',
    description='A simple module to encapsulate the built-in socket with struct.pack.',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='origamizyt',
    author_email='zhaoyitong18@163.com',
    url="https://github.com/origamizyt/StructuredSocket",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    py_modules=['structsock'],
    python_requires='>=3'
)