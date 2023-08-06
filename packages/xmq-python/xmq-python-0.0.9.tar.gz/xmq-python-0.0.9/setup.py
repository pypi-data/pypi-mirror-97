import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xmq-python",  # Replace with your own username
    version="0.0.9",
    author="neil",
    author_email="",
    description="mq的python封装包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'rocketmq-client-python==2.0.0',
        'pika==1.2.0',
    ],


    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
