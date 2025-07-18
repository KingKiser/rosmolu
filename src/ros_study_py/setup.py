from setuptools import find_packages, setup

package_name = 'ros_study_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='seonghwi',
    maintainer_email='ham9301@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "my_msg_test = ros_study_py.my_msg_test:main",
            "my_msg_subscriber = ros_study_py.my_msg_subscriber:main",
            "my_service_client = ros_study_py.my_service_client:main",
            "my_service_server = ros_study_py.my_service_server:main",
            "my_action_server = ros_study_py.my_action_server:main",
            "my_action_client = ros_study_py.my_action_client:main",
        ],
    },
)
