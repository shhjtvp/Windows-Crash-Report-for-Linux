from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crash-simulator",
    version="1.0.0",
    author="红蘑菇hj@bilibili.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shhjtvp/Windows-Crash-Report-for-Linux",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15",
        "psutil>=5.9"
    ],
    entry_points={
        "console_scripts": [
            "crash-sim = crash_sim.main:main",   # 主启动命令
            "crash-sim-setup = crash_sim.setup_utils:interactive_setup"  # 配置命令
        ]
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)