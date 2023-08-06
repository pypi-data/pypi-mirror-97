from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(
    name='subc',
    version='0.4.1',
    description='CLI sub-command library',
    long_description=long_description,
    url='https://git.sr.ht/~brenns10/subc',
    author='Stephen Brennan',
    author_email='stephen@brennan.io',
    license='Revised BSD',
    py_modules=['subc'],
    packages=find_packages(include=["subc", "subc.*"]),
    package_data={
        'subc': ['py.typed'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='arguments sub-command command',
)
