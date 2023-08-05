import setuptools

with open("README.md", "r",encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="Suluoya",
    version="1.7.1",
    author="Suluoya",
    author_email="1931960436@qq.com",
    maintainer='Suluoya',
    maintainer_email='1931960436@qq.com',
    description="Suluoya",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests',
                    'pandas',
                    'beautifulsoup4',
                    'translators == 4.7.9',
                    'fuzzywuzzy == 0.18.0',
                    'ngender == 0.1.1',
                    'MyQR == 2.3.1',
                    'pyforest == 1.0.3',
                    'wget == 3.2',
                    'urllib3',
                    'you-get == 0.4.1488',
                    'goose3 == 3.1.6',
                    'pandas_profiling == 2.9.0',
                    'flashtext == 2.7',
                    'textblob == 0.15.3',
                    'snownlp == 0.12.3',
                    'progressbar == 2.5',
                    'tqdm == 4.52.0',
                    'pyttsx3',
                    'textract',
                    'newspaper3k',
                    'baostock',
                    'parsel',
                    'pretty_errors',
                    'fake_useragent',
                    'lunar_python',
                    'pandasgui',
                    'sweetviz'
                    ]
)
