# python3 setup.py sdist upload -r testpypi (upload - test)
# pip3 install -i https://test.pypi.org/simple/ image_helpers==0.1.0 (download - test)

# Upload PyPi
# pip3 install twine
# python3 setup.py sdist bdist_wheel
# twine check dist/*
# python3 -m twine upload --repository pypi dist/*

from distutils.core import setup
from setuptools import find_packages


setup(
    name='image_helpers',
    description='Pacote para manipulacao de imagens',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Pillow>=8.1.0',
        'requests>=2.25.0'
    ],
    url='',
    author='Gustavo Schaedler',
    author_email='gustavopoa@gmail.com',
    license='MIT',
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='python image resize resizing thumbnail',
)
