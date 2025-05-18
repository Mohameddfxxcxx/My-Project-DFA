from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dfa_visualizer',
    version='1.0.0',
    author='Mohamed El-sadek Mohamed',
    author_email='mohamed122074@gmail.com',
    description='A web-based visualizer for DFA that recognizes "101" substring',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Mohameddfxxcxx/dfa-visualizer',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>=2.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Education',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'dfa-visualizer=dfa_visualizer.app:create_app',
        ],
    },
)