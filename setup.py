from setuptools import setup, find_packages

with open('README.md', mode='rt', encoding='utf-8') as f:
    long_desc: str = f.read()


# Setup module
setup(
    # Module name
    name="discord.py-i18n",
    # Module version
    version="0.1.0",
    # License - MIT!
    license='MIT',
    # Author (Github username)
    author="Lapis0875",
    # Author`s email.
    author_email="lapis0875@kakao.com",
    # Short description
    description="i18n support library on discord.ext.commands",
    # Long description in REAMDME.md
    long_description=long_desc,
    long_description_content_type='text/markdown',
    # Project urls
    project_urls={
        'Source': 'https://github.com/Lapis0875/discordpy_i18n/',
        'Tracker': 'https://github.com/Lapis0875/discordpy_i18n/issues/',
        'Funding': 'https://www.patreon.com/lapis0875'
    },
    # Include module directory
    packages=find_packages(),
    # Dependencies
    install_requires=["wheel>=0.36.2", "aiohttp>=3.7.3", "discord.py>=1.7.1"],
    # Module`s python requirement
    python_requires=">=3.7",
    # Keywords about the module
    keywords=["discord api", "discord.py", "i18n", "discord.ext.commands"],
    # Tags about the module
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
