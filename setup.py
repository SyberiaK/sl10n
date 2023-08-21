from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='sl10n',
    version='0.1.0.2',
    description='Static localization system that reduces a headache of working with localization',
    package_dir={'sl10n': 'sl10n'},
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SyberiaK/sl10n',
    author='SyberiaK',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Localization',
        'Topic :: Text Processing :: Linguistic',
        'Typing :: Typed'
    ],
    extras_require={
        'dev': ['pytest>=7.4.0', 'simplejson>=3.19.1', 'ujson>=5.8.0', 'twine>=4.0.2'],
    },
    python_requires='>=3.8',
)
