from setuptools import setup

setup(
    name='kenobi-hello',
    version='1.0.0',
    description='Kenobi\'s Hello World',
    url='',
    author='Guilherme Cartier',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    packages=['kenobi_hello'],
    entry_points={
        'console_scripts': [
            'kenobi=kenobi_hello.__main__:main'
        ]

    },
    author_email='gcartier94@gmail.com'
)
