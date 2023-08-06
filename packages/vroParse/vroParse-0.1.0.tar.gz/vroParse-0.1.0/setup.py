from setuptools import setup, find_packages

# Load the README file.
#with open(file="README.md", mode="r") as readme_handle:
#    long_description = readme_handle.read()
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='vroParse',
    author='Jim Sadlek',
    author_email='sadlekj@vmware.com',
    version='0.1.0',
    license='MIT',

    # Here is a small description of the library. This appears
    # when someone searches for the library on https://pypi.org/search.
    description='Parses scriptable tasks out of vRO Workflow XML, saves them as descrete files for editing and SCC, and imports edits in code back into XML.',

    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/nhlpens66/vroParse',
    keywords='sigma coding, governments, finance, APIs',
    packages=find_packages(),
    entry_points={ 
        'console_scripts': [ 
            'parsevro = parsevro.parsevro:main',
            'updatevro = updatevro.updatevro:main'
        ] 
    },

    # I also have some package data, like photos and JSON files, so
    # I want to include those as well.
    include_package_data=False,

    # Here I can specify the python version necessary to run this library.
    python_requires='>=3.7',

    # Additional classifiers that give some characteristics about the package.
    # For a complete list go to https://pypi.org/classifiers/.
    classifiers=[

        # I can say what phase of development my library is in.
        'Development Status :: 3 - Alpha',

        # Here I'll add the audience this library is intended for.
        'Intended Audience :: Developers',
        #'Intended Audience :: CI/CD',
        #'Intended Audience :: DevOps',

        # Here I'll define the license that guides my library.
        'License :: OSI Approved :: MIT License',

        # Here I'll note that package was written in English.
        'Natural Language :: English',

        # Here I'll note that any operating system can use it.
        'Operating System :: OS Independent',

        # Here I'll specify the version of Python it uses.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',

        # Here are the topics that my library covers.
        #'Topic :: Parse XML',
        #'Topic :: vRealize',
        #'Topic :: VMware'

    ]
)
