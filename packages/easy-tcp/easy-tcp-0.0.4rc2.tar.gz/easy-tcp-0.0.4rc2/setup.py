from setuptools import setup, Extension

try:
    from Cython.Build import cythonize
except ImportError:
    user_cython = False
else:
    use_cython = True

with open("README.md", "r") as fh:
    long_description = fh.read()

if use_cython:
    ext_modules = cythonize(
        Extension("easy_tcp",
                  sources=[
                      "process.c",
                      "server.c",
                      "cython_src/server.pyx"
                  ],
                  )
    )
else:
    ext_modules = [Extension(
        "easy_tcp",
        ["cython_src/process.c", "cython_src/server.c", ]
    )]



setup(
    name="easy-tcp",
    version="0.0.4rc2",
    description="Python TCP WSGI Server",
    packages=["easy_tcp", "cython_src"],
    install_requires=[
        "cython"
    ],
    zip_safe=False,
    ext_modules=ext_modules,
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
