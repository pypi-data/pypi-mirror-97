from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]


setup(
    name="FacebookMessengerAnalyzer", # Replace with your own username
    version="0.0.1",
    author="Marcin Zegarmistrz",
    description="A librayr which will help you easily run some simple Data Analytics on your Facebook Messenger Data ",
    url="https://github.com/zegarmm001/FacebookMessengerAnalyzer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6",
    install_require=["pandas","nltk","matplotlit"]
)