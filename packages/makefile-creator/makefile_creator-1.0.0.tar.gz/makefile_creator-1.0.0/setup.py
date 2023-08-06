import setuptools
import makefile_creator.config


with open("README.md", "r") as fh:
    long_description = fh.read()
    fh.close()


setuptools.setup(
    name=makefile_creator.config.PACKAGE_NAME,
    version=makefile_creator.config.VERSION,
    author="Romulus-Emanuel Ruja",
    author_email="romulus-emanuel.ruja@tutanota.com",
    description="MakeFile-Creator for makefiles management in C/C++ projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/m3sserschmitt/MakeFile-Creator.git",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: MIT License",
        'Natural Language :: English'
    ],
    license='MIT License',
    platforms='Linux',
    python_requires='>=3.6',
)

print('[+] Set up', makefile_creator.config.PACKAGE_NAME, 'version', makefile_creator.config.VERSION)
