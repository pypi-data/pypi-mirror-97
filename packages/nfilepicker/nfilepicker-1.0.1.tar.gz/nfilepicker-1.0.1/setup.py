from setuptools import setup

def readme():
    with open('README.md') as file:
        README = file.read()
    return README


setup(
    name='nfilepicker',
    version='1.0.1',
    description='A Python package that creates a file/folder chooser with ncurses.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Python3-8/nfilepicker',
    author='Pranav Balaji Pooruli',
    author_email='pranav.pooruli@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    packages=['nfilepicker'],
    include_package_data=True,
    install_requires=['pick'],
)
