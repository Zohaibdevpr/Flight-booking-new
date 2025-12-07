"""
Setup configuration for Flight Booking System.
"""

from setuptools import setup, find_packages

setup(
    name="flight-booking-solid",
    version="1.0.0",
    description="Complete Flight Booking System demonstrating all SOLID principles in Python",
    author="SOLID Principles Demo",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "mypy>=0.990",
            "flake8>=4.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "flight-booking=main:main",
        ]
    },
)
