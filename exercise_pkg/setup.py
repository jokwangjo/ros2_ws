from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'exercise_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name),glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jokwangjo',
    maintainer_email='jokwangjo@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'exercise1= exercise_pkg.exercise1:main',
            'exercise2= exercise_pkg.exercise2:main',
            'exercise3= exercise_pkg.exercise3:main',
        ],
    },
)
