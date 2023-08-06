from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='docscraper',
    version='0.1.4',
    description='a web crawler to scrape documents from websites',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://docscraper.readthedocs.io/en/latest/',
    author='Patrick Ryan',
    author_email='pryan@stoneturn.com',
    license='MIT',
    install_requires=[
        'openpyxl',
        'numpy>=1.16.5 ',
        'pandas',
        'scrapy',
    ],
    packages=[
        'docscraper',
    ],
    test_suite='tests',
    zip_safe=False,
)