import setuptools

setuptools.setup(
    name="benproto",
    version="1.0.7",
    license='BSD 3-Clause License',
    author="benproto",
    author_email="qjadn0914@naver.com",
    description="for stock use grpc proto",
    long_description=open('README.md').read(),
    url="https://github.com/gobenpark",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: BSD License"
    ],
)