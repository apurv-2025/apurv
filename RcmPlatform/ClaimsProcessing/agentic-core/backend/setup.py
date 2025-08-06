from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agentic-core",
    version="1.0.0",
    author="Agentic Core Team",
    author_email="team@agentic.core",
    description="Reusable AI Agent Framework for intelligent automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agentic/core",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.22.0",
        "pydantic>=2.0.0",
        "sqlalchemy>=2.0.0",
        "alembic>=1.11.0",
        "psycopg2-binary>=2.9.0",
        "redis>=4.5.0",
        "httpx>=0.24.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.6",
        "celery>=5.3.0",
        "prometheus-client>=0.17.0",
        "structlog>=23.1.0",
        "tenacity>=8.2.0",
        "pydantic-settings>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.2.0",
            "mkdocstrings[python]>=0.22.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agentic=agentic_core.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "agentic_core": [
            "config/*.yaml",
            "config/*.json",
            "templates/*.html",
            "static/*",
        ],
    },
) 