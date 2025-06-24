from setuptools import find_packages, setup
import glob
import os

package_name = "opencv_py"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ('share/' + package_name + '/param', glob.glob(os.path.join('param', '*.yaml'))),
    ],
    install_requires=["setuptools", 'opencv-python'],
    zip_safe=True,
    maintainer="user",
    maintainer_email="user@todo.todo",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "image_publisher = source.img_pub:main",
            "hough_transform = source.hough_transform:main",
            "yolo8 = source.yolo8:main",
            "personmosaic = source.personmosaic:main",
            "molu = source.molu:main",
            "moluya = source.molu_yaml:main",
            'grayscale = source.grayscale:main',
            'saveimg = source.saveimg:main',
            'imageconverter = source.imageconverter:main',
        ],
    },
)
