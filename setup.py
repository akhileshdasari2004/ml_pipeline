from setuptools import setup, find_packages

setup(
    name="training_bot",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.20.0",
        "google-generativeai>=0.5.0",
        "pydantic>=2.0.0",
        "pypdf2>=3.0.0",
        "python-docx>=1.0.0",
        "pandas>=2.0.0",
        "pyarrow>=14.0.0",
        "httpx>=0.25.0",
        "beautifulsoup4>=4.12.0",
        "aiofiles>=23.0.0",
        "streamlit>=1.28.0",
        "plotly>=5.18.0",
        "click>=8.1.0",
        "lingua-language-detector",
        "better-profanity",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "training-bot=training_bot.interfaces.cli:cli",
        ],
    },
)
