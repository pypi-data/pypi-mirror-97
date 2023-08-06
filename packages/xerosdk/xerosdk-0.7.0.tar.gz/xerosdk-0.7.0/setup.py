import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name="xerosdk",
    version="0.7.0",
    author="Ashwin T",
    author_email="ashwin.t@fyle.in",
    description="Python SDK to access Xero APIs",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['xero', 'api', 'python', 'sdk'],
    url="https://github.com/fylein/xero-sdk-py",
    packages=setuptools.find_packages(),
    install_requires=['requests==2.22.0'],
    classifiers=[
        "Topic :: Internet :: WWW/HTTP",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
