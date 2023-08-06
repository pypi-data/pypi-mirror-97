from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='classicML-python',
    version='0.6',
    description='An easy-to-use ML framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Steve R. Sun',
    author_email='s1638650145@gmail.com',
    url='https://github.com/sun1638650145/classicML',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    license='Apache Software License',
    install_requires=[
        'h5py>=2.10.0, <=3.1.0',
        'matplotlib>=3.3.2, <=3.3.4',
        'numpy>=1.19.2, <=1.19.4',
        'pandas>=1.1.3, <=1.1.4',
        'psutil>=5.7.2',
    ],
    python_requires='>=3.6',
)
