import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read().replace("](", "](https://raw.githubusercontent.com/FarisHijazi/deblack/master/")


setuptools.setup(
    name="deblack",
    version="0.0.2",
    description="Script to remove black frames from a video",
    long_description=long_description,
    url="https://github.com/FarisHijazi/deblack",
    author="Faris Hijazi",
    author_email="theefaris@gmail.com",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "ffmpeg-python",
    ],
    keywords="ffmpeg script video black frames",
    entry_points={
        "console_scripts": [
            "deblack=deblack.deblack:main",
        ]
    },
)
