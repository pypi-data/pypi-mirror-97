from setuptools import setup


SHORT_DESCRIPTION = 'Testing framework for Foliant'

try:
    with open('README.md', encoding='utf8') as readme:
        LONG_DESCRIPTION = readme.read()

except FileNotFoundError:
    LONG_DESCRIPTION = SHORT_DESCRIPTION


setup(
    name='foliantcontrib.test_framework',
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    version='0.1.3',
    author='Daniil Minukhin',
    author_email='ddddsa@gmail.com',
    url='https://github.com/foliant-docs/foliantcontrib.test_framework',
    packages=['foliant_test'],
    license='MIT',
    platforms='any',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Documentation",
        "Topic :: Utilities",
    ]
)
