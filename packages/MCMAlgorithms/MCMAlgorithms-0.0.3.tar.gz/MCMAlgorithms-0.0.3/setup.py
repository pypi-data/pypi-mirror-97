from setuptools import setup, find_packages
VERSION = '0.0.3'
tests_require = []
install_requires = ['numpy>=1.18.1', 'pandas>=1.0.3', 'scipy>=1.4.1']
setup(name='MCMAlgorithms', # 模块名称
      url='https://github.com/XHJ-TS9527/MCM-algorithms',  # 项目包的地址
      author="TS9527",  # Pypi用户名称
      author_email='scutee_xhj_ts9527@126.com',  # Pypi用户的邮箱
      keywords='python mathematical modeling',
      description='Package for mathematical modeling competitions. This package include some commonly used MCM algorithms.',
      license='MIT',  # 开源许可证类型
      classifiers=[
          'Operating System :: OS Independent',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Software Development',
          'Programming Language :: Python :: 3',
      ],
      version=VERSION,
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='runtests.runtests',
      extras_require={'test': tests_require},
      entry_points={'nose.plugins': [] },
      packages=find_packages(),
      python_requires='>=3.6',
)