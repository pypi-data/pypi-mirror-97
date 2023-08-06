from setuptools import setup, find_packages
from scanimage_webui.libs.setuptools import get_file_content, get_file_content_as_list


packages = find_packages()
print(f"Found packages: {packages}")
VERSION = get_file_content("scanimage_webui/VERSION")
INSTALL_REQUIRES = get_file_content_as_list("requirements.txt")
DOCUMENTATION_MD = get_file_content("README.md")

setup(
    name='scanimage-webui',
    version=VERSION,
    license='MIT',
    author='Ales Adamek',
    author_email='alda78@seznam.cz',
    description='WEB UI for SANE scanimage command.',
    long_description=DOCUMENTATION_MD,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/alda78/scanimage-webui',
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,  # MANIFEST.in
    zip_safe=False,  # aby se spravne vycitala statika pridana pomoci MANIFEST.in
    entry_points={
        'console_scripts': [
            'scanimage-webui=scanimage_webui.main:main',
        ],
    },
)
