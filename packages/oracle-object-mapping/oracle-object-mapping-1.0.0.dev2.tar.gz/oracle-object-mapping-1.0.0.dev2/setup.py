"""Setup file."""

import re

import setuptools

with open('oracle_object_mapping/__init__.py', 'rt', encoding='utf8') as f:
    r = re.search(r"__version__ = '(.*?)'", f.read())
    assert r is not None
    version = r.group(1)

with open('oracle_object_mapping/__init__.py', 'rt', encoding='utf8') as f:
    r = re.search(r'"""(.*?)"""', f.read())
    assert r is not None
    description = r.group(1)

with open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with open('requirements.txt', 'rt', encoding='utf8') as f:
    install_requires = f.read().strip().split('\n')
with open('requirements-lint.txt', 'rt', encoding='utf8') as f:
    lint_requires = f.read().strip().split('\n')

setuptools.setup(
    name='oracle-object-mapping',
    version=version,
    author='Fábio Domingues',
    author_email='fabio.a.domingues@gmail.com',
    license='MIT',
    description=description,
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/domingues/oracle-object-mapping',
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    extras_require={
        'lint': lint_requires,
    },
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
    ],
)
