import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="VirtualKey",
    version="0.0.4",
    author="bode135",
    author_email='2248270222@qq.com', # 作者邮箱
    description="VirtualKey with ctypes. 更新避免lol的屏蔽",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/bode135/VirtualKey_with_Ctypes', # 主页链接
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pywin32', 'bdtime', 'keyboard'], # 依赖模块
)
