from setuptools import setup

with open('README.md') as f:
    longdescription = f.read()
setup(
    name='tstpkg',
    version='0.0.1',
    description='testing pip packaging',
    long_description=longdescription,
    long_description_content_type='text/markdown',
    py_modules=['fstringtest'],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Development Status :: 1 - Planning",
        "Operating System :: Microsoft :: Windows"
    ],
    url='https://github.com/chetu181/testPackage',
    author='Chaithanya',
    author_email='csbasrur@smu.edu.sg'
)