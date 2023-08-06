import setuptools

setuptools.setup(
    name='bsv',
    version=0.6,
    description='spider project to get buy_sell_volume from 4 Futures Exchanges in Chinese Mainland',
    url="https://gitee.com/ragnaros27/bsv",
    packages=setuptools.find_packages(),
    author='ragnaros27',
    author_email='gooddunk@163.com',
    project_urls={"Code": "https://gitee.com/ragnaros27/bsv",},
    install_requires=['beautifulsoup4==4.8.1',
                      'lxml == 4.4.2',
                      'pandas == 0.25.3',
                      'requests==2.22.0',
                      'click==7.1.2',
                      ],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
