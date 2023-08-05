import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyembroidery",
    version="1.4.27",
    author="Tatarize",
    author_email="tatarize@gmail.com",
    description="Embroidery IO library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EmbroidePy/pyembroidery",
    packages=setuptools.find_packages(),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ),
)