from setuptools import setup, find_packages


setup(
    name='BIDS_stb',
    version='0.0.2',
    author='Chris C. Camp',
    author_email='chrisclaycamp@gmail.com',
    description='Small function to produce a set of single trial beta models from a BIDS compliant statistical model.',
    url='https://github.com/nimh-comppsych/BIDS_stb',
    py_modules=find_packages(),
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        BIDS_stb=bids_stb:stb_model
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
    ]
)
