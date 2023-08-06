from setuptools import find_packages, setup

setup(
    name='pacote-python-test',
    packages=find_packages(),
    version='1.1.0',
    description='Descrição curta do meu pacote',
    long_description='Longa descrição do meu pacote',
    author='Leonardo Holanda',
    author_email='meu@email.com',
    url='',
    install_requires=[],
    license='MIT',
    keywords=['dev', 'web'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)