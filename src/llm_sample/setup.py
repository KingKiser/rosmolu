from setuptools import find_packages, setup
import glob
import os

package_name = 'llm_sample'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob.glob(os.path.join('launch', '*.launch.py'))),
        ('share/' + package_name + '/param', glob.glob(os.path.join('param', '*.yaml'))),
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
            "gemini_sample = llm_sample.gemini_sample:main",
            "gemini_chat = llm_sample.gemini_chat:main",
            "gemini_call = llm_sample.gemini_call:main",
        ],
    },
)
