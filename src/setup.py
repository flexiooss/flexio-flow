from setuptools import setup

setup(
    name='flexio-flow',
    version='0.0.0',
    packages=['', 'tests', 'tests.Schemes', 'tests.Schemes.Package', 'tests.FlexioFlow', 'tests.FlexioFlow.Actions',
              'utils', 'Schemes', 'Schemes.Maven', 'Schemes.Docker', 'Schemes.Package', 'Schemes.Composer',
              'Exceptions', 'FlexioFlow', 'FlexioFlow.Actions', 'VersionControl', 'VersionControl.GitFlow',
              'VersionControl.GitFlow.Branches', 'VersionControl.GitFlow.Branches.Hotfix',
              'VersionControl.GitFlow.Branches.Release'],
    package_dir={'': 'src'},
    url='http://flexio.fr',
    license='Apache License 2.0',
    author='thomas',
    author_email='',
    description=''
)
