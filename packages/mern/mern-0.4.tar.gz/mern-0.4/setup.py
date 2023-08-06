from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
        return README


setup(
    name='mern',
    packages=['mern'],
    version='0.4',
    description=('data pre-processing library'),
    long_description=readme(),
    long_description_content_type="text/markdown",
    license='MIT',
    author='mrxxx04',
    author_email='rizkimaulana348@gmail.com',
    url='https://github.com/bluenet-analytica/mern',
    download_url='https://github.com/bluenet-analytica/mern/archive/v.0.1.zip',
    keywords=['machine-learning', 'surpervied-learning',
              'artificial-intelegence'],
    install_requires=[
        'numpy',
        'nltk',
        'scikit-learn'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
