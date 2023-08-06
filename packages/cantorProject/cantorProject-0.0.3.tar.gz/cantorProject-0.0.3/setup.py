import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cantorProject", # Replace with your own username
    version="0.0.3",
    author="V Abhijith Rao",
    author_email="varsg007@gmail.com",
    description="A set of tools to numerically solve differential equations using Neural Networks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VANRao-Stack/cantorProject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'tensorflow>=2.4.0',
        'tensorflow_probability>=0.12.0',
        'numpy>=1.19.4',
        'scipy>=1.4.1'
        ]
)
