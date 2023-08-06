import setuptools, os

readme_path = os.path.join(os.getcwd(), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r") as f:
        long_description = f.read()
else:
    long_description = 'dailytask'

setuptools.setup(
    name="dailytask",
    version="0.0.8",
    author="Kristof",
    description="dailytask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/py_daily_task",
    packages=setuptools.find_packages(),
    install_requires=[
        'colored-logs>=0.2.10',
        'kcu>=0.0.65',
        'noraise>=0.0.9',
        'stopit>=1.1.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)