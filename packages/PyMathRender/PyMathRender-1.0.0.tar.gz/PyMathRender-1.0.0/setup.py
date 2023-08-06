from setuptools import setup,find_packages
setup(
    name='PyMathRender',
    version='1.0.0',
    description='Pretty rendering method for mathematic functions',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/donno2048/Maths',
    packages=find_packages(),
    license='MIT',
    author='Elisha Hollander',
    classifiers=['Programming Language :: Python :: 3'],
    install_requires=['matplotlib']
)
