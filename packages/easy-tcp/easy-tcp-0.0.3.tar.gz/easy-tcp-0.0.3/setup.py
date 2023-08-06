from setuptools import setup, Extension
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="easy-tcp",
    version="0.0.3",
    description="Python TCP WSGI Server",
    packages=["easy_tcp"],
    install_requires=[
        "cython"
    ],
    zip_safe=False,
    ext_modules=cythonize(
        Extension("server",
            sources=[
                "process.c",
                "server.c",
                "cython_src/server.pyx"
            ],
        )
    ),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unix",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joegasewicz/easy-tcp",
    author="Joe Gasewicz",
    author_email="joegasewicz@gmail.com",
)
