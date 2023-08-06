from setuptools import setup, find_packages

VERSION = '1.1.1' 
DESCRIPTION = 'o7 Roblox Account Generator'
LONG_DESCRIPTION = "Generates roblox accounts for you. o7 Project https://github.com/o7-Fire/Roblox-Bot-Tool"

setup(
        name="RobloxAccountMaker", 
        version=VERSION,
        author="o7-Fire",
        author_email="<fireo7incorporated@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["selenium"],
        
        keywords=['python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ])
