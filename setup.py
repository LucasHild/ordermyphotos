from setuptools import setup

# with open("README.md") as f:
#     long_description = f.read()

setup(
    name="ordermyphotos",
    version="1.0.0",
    description="Order my photos by date",
    # long_description=long_description,
    license="MIT",
    author="Lucas Hild",
    author_email="contact@lucas-hild.de",
    url="https://lucas-hild.de",
    py_modules=["ordermyphotos"],
    install_requires=[
        "exifread",
        "click"
    ],
    entry_points="""
        [console_scripts]
        ordermyphotos=ordermyphotos:cli
    """
)