from setuptools import setup

requirements = []
with open('requirements.txt', 'r') as fh:
    for line in fh:
        requirements.append(line.strip())

setup(
    name='vlute_faces_services',
    version='0.0.3',
    description='',
    url='http://fit.vlute.edu.vn',
    author='truongtpa',
    author_email='truongtpa@vlute.edu.vn',
    license='MIT',
    packages=['vlute_faces_services'],
    zip_safe=False,
    install_requires=requirements
)