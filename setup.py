

import setuptools

setuptools.setup(
    name='QMData-Tools',
    version='v0.5.4',
    author='Andronet',
    author_email='',
    packages=['bin', 'utils', 'gaussian09', 'reanet', 'openmolcas', 'Constants', 'orca', 'Old_scripts'],
    url="https://github.com/AndreyShtyrov/QMData-Tools.git",
    scripts=['bin/check_optimization', 'bin/Convert_gauss_to_molcas', 'bin/extract_orb', 'bin/lqdel',
             'bin/reshape_hessian', 'bin/show_avaliable_ants', 'bin/convert_to_molden', 'bin/get_optimized_geom',
             'Old_scripts/calculate_stat_sum.py', 'Old_scripts/Calc_freq.py', 'Old_scripts/diff_hessian.py'],
    license='',
    install_requires=['numpy', 'termcolor', 'pathlib' ],
    description=''
)
