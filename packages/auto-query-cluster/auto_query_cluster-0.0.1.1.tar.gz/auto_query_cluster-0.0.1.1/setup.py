from setuptools import setup, find_packages
setup(
    name='auto_query_cluster',
    version='0.0.1.1',
    description='Auto Query Cluster',
    long_description='Auto Query Cluster',
    long_description_content_type="text/markdown",
    author='fubo',
    author_email='fb_linux@163.com',
    url='https://gitee.com/fubo_linux/auto_query_cluster',
    packages=find_packages(where='.', exclude=(), include=('*',)),
    package_data={
        "auto_query_cluster": [
            "sent2vec.models/dict",
            "sent2vec.models/*",
            "sent2vec.models/dict/*"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'nlp-nn>=0.0.3.0',
    ],
    python_requires='>=3.6'
)
