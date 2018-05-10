from setuptools import setup

setup(
    name='eosio-log2mq',
    version='0.1',
    packages=['log2mq'],
    url='https://github.com/eostea/log2mq',
    license='Apache License 2.0',
    author='strahe',
    author_email='a@tclabs.tech',
    install_requires=[
        'inotify>=0.2.9'
    ],
    entry_points={
            'console_scripts': [
                'log2mq = log2mq.core:main',
            ],
        },
    description='EOS.IO logfile to Message Queue(NSQ).'
)
