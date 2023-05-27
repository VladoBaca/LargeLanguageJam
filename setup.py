from setuptools import setup

setup(
    name="Large Language",
    python_requires='>=3.8',
    version="0.1.0",
    description="Large Language model from AI Alignment jam",
    author="HHJV",
    py_modules=["main"],
    install_requires=[
        "requests",
    ],
    tests_require=["pytest", "pytest-mock"],
    entry_points="""
        [console_scripts]
        main=main:cli
    """,
    test_suite="tests",
)
