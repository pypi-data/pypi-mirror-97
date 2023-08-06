import setuptools
from version import VERSION


with open("README.md", "r") as fh:
    long_description = fh.read()

DESCRIPTION = """
Python Reusable Functions. Reusable functions are categorized as csv_utils, PandasUtils etc.
"""[1:-1]

CLASSIFIERS = """
Programming Language :: Python :: 3
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Topic :: Software Development :: Testing
Development Status :: 5 - Production/Stable
"""[1:-1]

setuptools.setup(
    name="cqepyutils",
    version=VERSION,
    author="Sridhar VP",
    author_email="sridharvpmca@gmail.com",
    description="Cognitive Quality Engineer - Python Reusable Function Library",
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/cognitiveqe/cqepyutils/',
    keywords='Python Reusable Function Library',
    license='MIT',
    packages=setuptools.find_packages(),
    platforms='any',
    classifiers=CLASSIFIERS.splitlines(),
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'numpy',
        'requests',
        'robotframework',
        'robotframework-requests',
        'jinja2',
    ],
)
