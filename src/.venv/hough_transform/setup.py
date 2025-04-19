from setuptools import find_packages, setup
import glob
import os

package_name = "hough_transform"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ('share/' + package_name + '/param', glob.glob(os.path.join('param', '*.yaml'))),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="user",
    maintainer_email="user@todo.todo",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "image_publisher = hough_transform.img_pub:main",
            "hough_transform = hough_transform.hough_transform:main",
            "yolo8 = hough_transform.yolo8:main",
            "personmosaic = hough_transform.personmosaic:main",
            "molu = hough_transform.molu:main",
            "moluya = hough_transform.molu_yaml:main",
        ],
    },
)
