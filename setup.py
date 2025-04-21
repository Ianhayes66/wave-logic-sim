from setuptools import setup, find_packages

setup(
    name="wave_logic_sim",
    version="0.1.0",
    packages=find_packages(include=["wave_logic_sim", "wave_logic_sim.*"]),
    install_requires=["numpy", "matplotlib"],
    author="Ian Hayes",
    description="A simulation framework for wave-based computing (photonic + magnonic).",
    python_requires='>=3.7'
)
