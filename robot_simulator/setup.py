from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'robot_simulator'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Robot Engineer',
    maintainer_email='robot@example.com',
    description='A simple robot simulator package for ROS2 Humble.',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sensor_publisher = robot_simulator.sensor_publisher:main',
            'actuator_subscriber = robot_simulator.actuator_subscriber:main',
        ],
    },
)
