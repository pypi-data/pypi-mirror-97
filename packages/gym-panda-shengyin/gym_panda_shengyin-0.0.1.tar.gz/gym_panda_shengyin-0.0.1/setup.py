import setuptools
from pathlib import Path

setuptools.setup(
    name='gym_panda_shengyin',
    author="Shengyin Wang",
    author_email="shengyin.wang@hotmail.com",
    version='0.0.1',
    description="An OpenAI Gym Env for Panda",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(include="gym_panda_shengyin*"),
    install_requires=['gym', 'pybullet', 'numpy'],  # And any other dependencies foo needs
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    python_requires='>=3.6'
)