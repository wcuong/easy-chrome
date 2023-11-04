import setuptools

setuptools.setup(
    name="easy-chrome",
    version="2.0.0",
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
    keywords='easy-chrome chrome_driver selenium chrome',
    packages=setuptools.find_packages(),
    install_requires=open('requirements.txt', 'r').readlines(),
    python_requires=">=3.10",
)
