from setuptools import setup, find_packages

setup(
    name='llm_sdk',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'requests',

    ],
    description='A Python package for interacting with the LLM API.',
    author='Lucas Kulla',
    author_email='lucas.kulla@dkfz-heidelberg',
    url='https://github.com/lucaskulla/my_llm_sdk',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
