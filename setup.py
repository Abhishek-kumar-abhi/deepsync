from setuptools import setup, find_packages

setup(
    name="local-ai-helper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "speechrecognition>=3.10.0",
        "pyttsx3>=2.90",
        "pyaudio>=0.2.14",
        "ttkthemes>=3.2.2",
        "requests>=2.28.1",
    ],
    entry_points={
        "gui_scripts": [
            "local-ai-helper = gui.gui_app:main",
        ],
    },
)
