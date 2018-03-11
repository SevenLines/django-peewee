import os.path
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setupconf = dict(
    name='django-peewee',
    version="0.0.1",
    license='BSD',
    url='https://github.com/SevenLines/django-peewee/',
    author='Mikhail Katashevtsev',
    author_email='fables@yandex.ru',
    description=('Peewee to Django integration library'),
    long_description=read('README.rst'),
    packages=['django_peewee'],

    install_requires=['peewee>=3.0.1'],

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)

if __name__ == '__main__':
    setup(**setupconf)
