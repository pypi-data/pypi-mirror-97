import setuptools

# with open("README.md", 'r') as fd:
#     long_description = fd.read()

# python setup.py sdist bdist_wheel
# twine upload dist/*
# rm -rf build dist *.egg-info

setuptools.setup(
    name="minidict",
    version="0.0.1",
    author="RA",
    author_email="numpde@null.net",
    keywords="read-only python dict",
    description="Minimal read-only dictionary",
    long_description="Minimal read-only dictionary.",
    long_description_content_type="text/markdown",
    url="https://github.com/numpde/minidict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[''],

    # Required for includes in MANIFEST.in
    include_package_data=True,

    test_suite="nose.collector",
    tests_require=["nose"],
)
