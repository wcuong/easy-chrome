import setuptools
import os

setuptools.setup(
    name="easy-chrome",
    version="2.0.2",
    author="VanCuong",
    author_email="vuvancuong94@gmail.com",
    description="selenium chrome extension with shortcuts to control driver and element",
    long_description=open('README.md').read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS'
    ],
    license='MIT',
    keywords='easy chrome chrome_driver selenium chromedriver',
    packages=setuptools.find_packages(),
    install_requires=['selenium', 'webdriver-manager'],
    python_requires=">=3.9",
    long_description_content_type="text/markdown",
    project_urls={
        'Source': 'https://github.com/wcuong/easy-chrome',
    },
)
