from setuptools import setup, find_packages


version = '0.1dev'

version_inf = '''
--------------------------------
Installing reaflow version {v}
--------------------------------
'''.format(v=version)

print(version_inf)


setup(
    name='reaflow',
    version=version,
    author='lx Gui',
    author_email='guilixuan@gmail.cn',
    keywords=['bioinformatics', 'NGS', 'RNAseq'],
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'click',
    ],
    entry_points={
        'ExpBase': [
            "expression_filter=reaflow.expression.base:expression_filter",
        ]
    }

)

exit_inf = '''
--------------------------------
reaflow installation complete!
--------------------------------
'''

print(exit_inf)
