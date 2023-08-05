'''
@File       :   setup.py
@Author     :   Yiteng Zhang
@Time       :   2020-10
@Version    :   1.0
@Contact    :   zytfdu@icloud.com
@Dect       :   None
'''
 
from setuptools import setup, find_packages
 
setup(
    name = "matrixdifferential",
    version = "0.0.11",
    keywords = ("pip", "pyctlib"),
    description = "This is a mathematic calculation package for computing matrix differential",
    long_description = "This is a mathematic calculation package for computing matrix differential",
    license = "MIT Licence",
 
    url = "https://github.com/Bertie97/pyctlib/tree/main/pyctlib",
    author = "All contributors of PyCTLib",
    author_email = "zytfdu@icloud.com",
 
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy"]
)
