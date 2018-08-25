from setuptools import setup, find_packages


version = '0.1dev'

print '''
--------------------------------
Installing reaflow version {v}
--------------------------------
'''.format(v=version)


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
    # scripts=['scripts/reaflow'],
    entry_points={
        'ExpBase': [
            "base_expression_filter=reaflow.expression.base:expression_filter",
        ]
    }

)

print'''
--------------------------------
reaflow installation complete!
--------------------------------
'''
