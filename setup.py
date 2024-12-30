from setuptools import setup, find_packages

setup(
    name="data_transformation_api",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Unified Data Transformation and Validation API using FastAPI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/data_transformation_api",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "pandas",
        "pydantic",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "run-api=app.main:app",  # Command to run the API
        ],
    },
)
