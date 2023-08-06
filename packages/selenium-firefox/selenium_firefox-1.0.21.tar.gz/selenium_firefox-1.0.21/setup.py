import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selenium_firefox",
    version="1.0.21",
    author="Kovács Kristóf-Attila",
    description="selenium_firefox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/selenium_firefox",
    packages=setuptools.find_packages(),
    install_requires=[
        'geckodriver-autoinstaller>=0.1.0',
        'noraise>=0.0.9',
        'selenium>=3.141.0',
        'tldextract>=3.1.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)