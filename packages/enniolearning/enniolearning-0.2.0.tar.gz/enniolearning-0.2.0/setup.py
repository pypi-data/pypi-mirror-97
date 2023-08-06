from setuptools import setup

setup(
    name='enniolearning',
    version='0.2.0',
    author='Pierrick Baudet',
    author_email='pbaudet.enseirb@gmail.com',
    packages=['enniolearning', 'enniolearning.test'],
    license='see LICENSE.txt',
    url='https://github.com/Mara-tech/Ennio-Learning',
    description='A Machine Learning engine for MID music files, based on PyTorch framework.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'music21 >= 6.1.0',
        'torch >= 1.6.0',
        'numpy',
        'pandas',
        'matplotlib',
        'jordan_py >= 1.0.0'
    ]
)