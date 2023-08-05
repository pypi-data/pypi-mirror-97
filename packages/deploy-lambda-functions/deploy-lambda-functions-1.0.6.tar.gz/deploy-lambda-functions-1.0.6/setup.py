from setuptools import setup,find_packages, os

setup(
    name='deploy-lambda-functions',
    version= os.environ['CIRCLE_TAG'],
    description='Script to deploy lambda functions to AWS',
    url='https://github.com/redaptiveinc/deploy-lambda-functions',
    author='Mariano Gimenez',
    author_email='mariano.gimenez@agileengine.com',
    license='unlicense',
    zip_safe=False,
    packages = find_packages(),
    entry_points ={
        'console_scripts': [
            'deploy-lambda-functions = src.main:main'
        ]
    },
    install_requires = [
        'python-dotenv==0.10.3',
        'boto3==1.10.7',
        'botocore==1.13.9'

    ]
)
