from setuptools import setup

setup(
    name='WebProcessor',
    version='0.1.0',
    description='A example Python package',
    url='https://github.com/TheBlockNinja/WebProcessor',
    author='Seann Moser',
    author_email='seannsea@gmail.com',
    packages=['driver/WebProcessor','driver/Requirements'],
    install_requires=['beautifulsoup4==4.9.3',
                      'certifi==2020.12.5',
                      'chardet==4.0.0',
                      'idna==2.10',
                      'requests==2.25.1',
                      'selenium==3.141.0',
                      'soupsieve==2.2',
                      'urllib3==1.26.3'],

    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
)
