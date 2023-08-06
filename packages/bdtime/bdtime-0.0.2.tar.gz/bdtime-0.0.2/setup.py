import setuptools

with open("README.md", "r", encoding = 'utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="bdtime",
    version="0.0.2",
    author="bode135",
    author_email='2248270222@qq.com', # 作者邮箱
    description="bode\'s private time model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/bode135/pydamo', # 主页链接
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # install_requires=['pywin32', 'tqdm'], # 依赖模块
)
