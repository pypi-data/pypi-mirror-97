from setuptools import setup

setup(
    name='snacks',
    version='0.0.5',
    url='https://gitlab.com/mburkard/snacks',
    license='GNU General Public License v3 (GPLv3)',
    author='Matthew Burkard',
    author_email='matthewburkard@gmail.com',
    description='Wrapper to pika for an easier to use RabbitMq interface.',
    package_dir={'': 'src'},
    packages=['snacks'],
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    install_requires=['pika', 'dataclasses-json'],
    zip_safe=False
)
