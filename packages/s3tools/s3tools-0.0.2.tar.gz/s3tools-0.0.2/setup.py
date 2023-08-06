from setuptools import setup, find_packages

setup(
    name='s3tools',
    version='0.0.2',
    description='A simple Python package to upload/download objects to AWS S3',
    long_description_content_type='text/markdown',
    author='Hayman',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=['boto3', 'glog']
)
