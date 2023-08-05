from setuptools import setup, find_packages

VERSION = '1.5' 
DESCRIPTION = 'Package to standerdize and beautify matplotlib and seaborn graphs'
LONG_DESCRIPTION = 'Sets default for fonts, axes, color schemes, ticks, legend across matplotlib'

# Setting up
setup(
        name="pyintellify", 
        version=VERSION,
        author="Ansh Bordia",
        author_email="<ansh.bordial@intellify.com.au>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        py_modules = ["pyintellify"],
        package_dir={'': 'src'},
        install_requires=['matplotlib'],
        keywords=['python', 'matplotlib beautification'],
        classifiers= [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

print(find_packages())