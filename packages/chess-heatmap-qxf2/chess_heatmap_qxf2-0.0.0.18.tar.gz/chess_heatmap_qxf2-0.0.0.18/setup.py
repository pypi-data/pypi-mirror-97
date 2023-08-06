import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chess_heatmap_qxf2",
    version="0.0.0.18",
    author="Sravanti Tatiraju",
    author_email="sravanti.t25@gmail.com",
    description="Package to generate chess heatmaps from pgn files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
