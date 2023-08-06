from setuptools import setup


setup(
    name='demyst-cli',

    version='0.8.39',

    description='',
    long_description='',

    author='Demyst Data',
    author_email='info@demystdata.com',

    license='',
    entry_points='''
        [console_scripts]
        demyst=demyst.cli.command:cli
    ''',
    packages=['demyst.cli','demyst.cli.channel','demyst.cli.auth'],
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'demyst-common>=0.8.39',
        'click',
        'boto3',
        'botocore',
        'tabulate',
        'halo',
        'glom'
    ]
)
