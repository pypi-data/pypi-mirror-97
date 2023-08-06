from setuptools import setup

setup(
    name='WebProcessor',
    version='0.1.8',
    description='A package for loading websites and extracting information: THIS IS FOR EDUCATIONAL PURPOSES ONLY OR IF YOU HAVE CONSENT TO USE THAT SITES INFO!',
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
