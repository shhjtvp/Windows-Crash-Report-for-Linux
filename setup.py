from setuptools import setup, find_packages
import sys

class RiskAwareInstall(install):
    def run(self):
        warning = """
⚠️非正经程序，建议在虚拟机/非生产力环境下运行
本程序可能行为：
    • 主动终止/干扰系统进程
    • 模拟崩溃、注入异常、修改运行时状态
    • 产生不可预期的副作用（包括但不限于数据丢失） 

作者不对任何直接或间接损失负责
继续使用即表示您已理解并接受上述风险
"""
        print(warning)
        confirm = input("输入 'YES I UNDERSTAND' 继续安装: ").strip()
        if confirm != "YES I UNDERSTAND":
            print("安装已取消，安全第一喵ψ(｀∇´)ψ")
            sys.exit(1)
        super().run()

setup(
    name="crash-sim",
    version="Alpha 0.0.2",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "psutil>=5.9.0",  # 进程监控必需，比原生 os 更跨平台稳定
    ],
    extras_require={
        "gui": ["PyQt5>=5.15"],
    },
    entry_points={
        "console_scripts": [
            "crash-sim=crash_sim.main:main",
            "crash-sim-setup=crash_sim.setup_utils:interactive_setup",
        ],
    },
    author="Your Name",
    description="A robust crash simulation and process monitoring tool",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    cmdclass={"install": RiskAwareInstall},
)