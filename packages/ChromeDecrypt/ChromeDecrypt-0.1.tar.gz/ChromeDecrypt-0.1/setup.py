from setuptools import setup

setup(
    name="ChromeDecrypt",
    version=0.1,
    author="Lightman",
    author_email="L1ghtM3n@protonmail.com",
    description="Chrome logins, cookies, autofill, creditcards decryptor",
    url="https://github.com/L1ghtM4n",
    packages=["ChromeDecrypt"],
    install_requires=[
        "pycryptodome",
        "DPAPI"
      ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)