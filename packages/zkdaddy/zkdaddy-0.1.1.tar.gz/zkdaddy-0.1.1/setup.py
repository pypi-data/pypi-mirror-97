import os, shutil
from setuptools import setup, find_packages

# 移除构建的build文件夹
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(CUR_PATH, 'build')
if os.path.isdir(path):
    print('INFO del dir ', path)
    shutil.rmtree(path)
setup(
    url="https://github.com/siskinc/zkdaddy",
    name="zkdaddy",
    version="0.1.1",
    py_modules="zkdaddy",
    install_requires=['click==7.1.2', 'colorama==0.4.4', 'kazoo==2.8.0', 'pydantic==1.8.1', 'six==1.15.0',
                      'typing-extensions==3.7.4.3'],
    scripts=['main.py'],
    author="daryl",
    author_email="susecjh@gmail.com",
    packages=find_packages(),  # 包括在安装包内的Python包
    include_package_data=True,  # 启用清单文件MANIFEST.in,包含数据文件
    entry_points="""
    [console_scripts]
    zkdaddy=main:cli
    """
)
