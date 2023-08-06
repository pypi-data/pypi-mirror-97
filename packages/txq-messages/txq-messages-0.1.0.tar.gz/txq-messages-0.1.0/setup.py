from setuptools import setup


setup(
    name='txq-messages',
    zip_safe=True,
    version='0.1.0',
    description='Message prototypes for TXQ Framework',
    url='https://github.com/agratoth/txq-messages',
    maintainer='Anton Berdnikov',
    maintainer_email='agratoth@yandex.ru',
    packages=[
        'txq_messages'
    ],
    package_dir={'txq_messages': 'txq_messages'},
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.8',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
