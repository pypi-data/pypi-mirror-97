from setuptools import setup

setup(
    name='JiraLogin',
    version='1.0.3',
    author='Mason Hanson',
    author_email='UNKNOWN',
    packages=['jiralogin',],
    license='MIT License',
    description='A Jira login assistant that saves credentials for individual servers locally for future use.',
    long_description=open('README.txt').read(),
    keywords='jira atlassian authentication',
    install_requires=[
        "Jira >= 2.0.0",
    ]
)
