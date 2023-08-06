import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mkdocs-htmlproofer-plugin',
    version='0.1.0',
    description='A MkDocs plugin that validates URL in rendered HTML files',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown',
    url='https://github.com/manuzhang/mkdocs-htmlproofer-plugin',
    author='Manu Zhang',
    author_email='owenzhang1990@gmail.com',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'mkdocs>=0.17',
        'requests',
        'beautifulsoup4'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(exclude=['*.tests']),
    entry_points={
        'mkdocs.plugins': [
            'htmlproofer = htmlproofer.plugin:HtmlProoferPlugin'
        ]
    }
)
