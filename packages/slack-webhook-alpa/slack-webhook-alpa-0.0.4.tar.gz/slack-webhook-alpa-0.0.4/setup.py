import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slack-webhook-alpa", # Replace with your own username
    version="0.0.4",
    author="Albert Pang",
    author_email="alpaaccount@mac.com",
    description="Wrapper for slack_sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alpaalpa/slack-webhook",
    packages=setuptools.find_packages(),
    install_requires = [
        "requests",
        "slack_sdk"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
