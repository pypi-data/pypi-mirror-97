import setuptools
setuptools.setup(
    name="frostdb", # Replace with your own username
    version="0.0.1",
    author="ThatCoolDev",
    author_email="coffeeguyirl@gmail.com",
    description="An extremely fast and easy to use Key-Value database",
    url="https://github.com/frostythedumdum/frost.db-python",
    project_urls={
        "Bug Tracker": "https://github.com/frostythedumdum/frost.db-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
