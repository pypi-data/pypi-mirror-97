from setuptools import setup

setup(
    name="FirefoxDecrypt",
    version=0.2,
    author="Lightman",
    author_email="L1ghtM3n@protonmail.com",
    description="Decrypt firefox logins in one line (FireFoxDecrypt.DecryptLogins('logins.json', 'key4.db', 'your_masterpassword_if_exists'))",
    url="https://github.com/L1ghtM4n",
    packages=["FireFoxDecrypt"],
    install_requires=[
        "pycryptodome",
        "pyasn1"
      ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)