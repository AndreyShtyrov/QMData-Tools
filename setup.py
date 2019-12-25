

import setuptools

setuptools.setup(
    name='QMData-Tools',
    version='v0.5.12.00046',
    author='Andronet',
    author_email='',
    packages=setuptools.find_packages(),
    url="https://github.com/AndreyShtyrov/QMData-Tools.git",
    scripts=['bin/check_optimization', 'bin/bufferQM', 'bin/generate_input', 'bin/Convert_gauss_to_molcas', 'bin/extract_orb', 'bin/lqdel',
             'bin/reshape_hessian', 'bin/show_avaliable_ants', 'bin/convert_to_molden', 'bin/get_optimized_geom',
             'Old_scripts/calculate_stat_sum.py', 'Old_scripts/Calc_freq.py', 'Old_scripts/diff_hessian.py',
             'bin/generate_coords_for_hessian_calc', 'bin/analyse_outfile', 'bin/show_def'],
    license='',
    install_requires=['numpy', 'termcolor', 'pathlib', 'argparse', 'pyyaml', 'clipboard'],
    description=''
)
