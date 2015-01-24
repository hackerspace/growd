from setuptools import setup, find_packages

setup(
    name='growd',
    version='0.0.0',
    description='Plant monitoring and control library',
    #long_description='',
    #download_url='',
    url='https://github.com/mmilata/growd',
    author='Martin Milata',
    author_email='b42@srck.net',
    packages=find_packages(),
    scripts=[],
    install_requires=[],
    test_suite='nose.collector',
    tests_require=['nose'],
    #license='GPLv3'
)
