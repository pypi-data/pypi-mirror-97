import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pi-touch-gui",
    version="0.3.8",
    author="Edwin Wise",
    author_email="edwin@simreal.com",
    description="A graphic UI optimized for touch screens",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EdwinWiseOne/PiTouchGui",
    packages=setuptools.find_packages(),
    package_data={"": ["assets/*.png"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: Free for non-commercial use",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Home Automation",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.6',
    install_requires=['pygame'],
)
