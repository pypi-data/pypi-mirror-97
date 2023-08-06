import setuptools

setuptools.setup(
    name="today-calender",
    version="0.0.4",
    author="lindaye",
    author_email="454784911@qq.com",
    description="基于爬虫的历法查询工具",
    long_description="一个展示当日老黄历的命令行工具\n输入命令: td",
    url="https://github.com/stellaye/today",
    packages=["today"],
    entry_points={'console_scripts': [
            'td = today.main:main',
        ]},
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
