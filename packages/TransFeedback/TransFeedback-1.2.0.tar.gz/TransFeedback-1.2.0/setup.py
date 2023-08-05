from setuptools import setup

setup(
    name='TransFeedback',
    version='1.2.0',
    author='Eric Van Thorre',
    packages=['transfeedback'],
    install_requires=['openpyxl==3.0.2','requests','uuid'],
    entry_points={
        'console_scripts': [
        'translatefeedback = transfeedback.translateFeedback:main']
    })