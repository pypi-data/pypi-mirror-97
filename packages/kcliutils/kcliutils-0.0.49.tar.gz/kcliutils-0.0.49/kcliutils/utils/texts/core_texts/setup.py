setup = '''
import setuptools, os

readme_path = 'README.md'

if os.path.exists(readme_path):
    with open(readme_path, 'r') as f:
        long_description = f.read()
else:
    long_description = '[PACKAGE_NAME]'

setuptools.setup(
    name='[PACKAGE_NAME]',
    version='[PACKAGE_VERSION]',
    author='[AUTHOR]',
    description='[SHORT_DESCRIPTION]',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='[GIT_URL]',
    packages=setuptools.find_packages(),
    install_requires=[[DEPENDENCIES]],
    classifiers=[
        [PYTHON_CLASSIFIERS],
        'Operating System :: OS Independent',
    ],
    python_requires='>=[MIN_PYTHON_VERSION]',
)
'''.strip()