from setuptools import setup, find_packages

VERSION = '1.1.7' 
DESCRIPTION = 'A mini toolbox for moleuclar sequence analysis'
LONG_DESCRIPTION = 'A mini toolbox for moleuclar sequence analyses: calculate GC  content; get reverse complement sequence; count matched oligos'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="miniseqtoolbox", 
        version=VERSION,
        author="YuanLi",
        author_email="<ivon19571226@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'miniseqtoolbox'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
