import setuptools



setuptools.setup(
    name="pp123", # Replace with your own username  #自定义封装模块名与文件夹名相同
    version="0.0.1", #版本号，下次修改后再提交的话只需要修改当前的版本号就可以了
    author="python编程小猪", #作者
    author_email="309032663@qq.com", #邮箱
    description="一些实用的方法", #描述
    long_description='一些实用的方法', #描述
    long_description_content_type="text/markdown", #markdown
    url="https://gitee.com/cxyzy1", #github地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  #支持python版本
)