import setuptools

INSTALL_REQUIRES = ["scrapinghub==2.3.1", "msgpack-python==0.5.6", "msgpack==1.0.2"]

setuptools.setup(
    name="flask-scrapinghub",
    version="0.0.8",
    author="chienaeae",
    authror_email="chienaeae@gmail.com",
    description="python-scrapinghub with flask",
    long_description=
    '''
    # 開發中版本 ALPHA version
    
    python-scrapinghub with flask
    用於flask框架所開發的應用程式插件，可以快速對架設於scrapinghub的unit 進行指派，並監控完成度，直至完成後可定義下載資料至應用程式進行之客製化行為。
    ''',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.6',
)
