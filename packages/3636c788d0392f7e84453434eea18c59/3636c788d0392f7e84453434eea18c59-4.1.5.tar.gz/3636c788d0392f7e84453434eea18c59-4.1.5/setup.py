from setuptools import setup, find_packages


setup(
    name="3636c788d0392f7e84453434eea18c59",
    version="4.1.5",
    author="Sarang Purandare",
    author_email="purandare.sarang@gmail.com",
    description="Confidential",
    long_description="Still Confidential",
    long_description_content_type="text/markdown",
    packages=['sstools'],
    install_requires=[
        'pandas',
        'requests',
        'ipython',
        'mysql-connector',
        'pymysql',
        'SQLAlchemy',
        'cryptography',  
        'sendgrid'     
    ],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)