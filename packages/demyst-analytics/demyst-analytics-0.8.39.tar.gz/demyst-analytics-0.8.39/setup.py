from setuptools import setup

type_guesser_reqs = [
    'keras==2.3.1',
    'tensorflow==2.0.0',
    'usaddress'
    ]

setup(
    name='demyst-analytics',

    version='0.8.39',

    description='',
    long_description='',

    author='Demyst Data',
    author_email='info@demystdata.com',

    license='',

    packages=['demyst.analytics'],
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'demyst-common>=0.8.39',
        'yattag',
        'IPython',
        'tqdm',
        'ipywidgets',
        'pandas',
        'pandas_schema'
    ],
    extras_require={
        'type_guesser': type_guesser_reqs,
        'all': type_guesser_reqs
    }
)
