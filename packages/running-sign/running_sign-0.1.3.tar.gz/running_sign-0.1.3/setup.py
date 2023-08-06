from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='running_sign',
    version='0.1.3',
    description='progress indicator while program running',
    url='https://github.com/jryzj/running_sign',
    author='Jerry Zang',
    author_email='2381002887@qq.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha'   
    ],
    keywords='progress, indicator, sign, program, running',
    packages= ['running_sign'],
    install_requires=['apscheduler'],
    python_requires= '>=3',
)