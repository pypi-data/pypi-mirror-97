from setuptools import setup, find_packages

readme = """
This is a simple log module that can be used in UTC time. For detailed usage, refer to the README on github url.
"""

setup(
    name='utc-simple-log',
    version='0.0.4',
    packages=find_packages(),
    description='Simple log wrapping python logging module',
    long_description=readme,
    license='MIT',
    author='Park Donghyeon',
    author_email='emma415g@gmail.com',
    url='https://github.com/ppd0523/utc-simple-log.git',
    install_requires=['pytz'],
    classifiers=["Programming Language :: Python :: 3.8",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 ],
    python_requires='>=3.8'
)