from setuptools import setup, find_packages


VERSION = '0.1'
DESCRIPTION = 'Python Api Client For UpStorage App.'
LONG_DESCRIPTION = 'A package that helps to call UpStorage Api Easily.'

# Setting up
setup(
    name="UpStorageApiClient",
    version=VERSION,
    author="Sakib (Florian Dedov)",
    author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'storage', 'api', 'upstorage', 'UpStorageApiClient'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)