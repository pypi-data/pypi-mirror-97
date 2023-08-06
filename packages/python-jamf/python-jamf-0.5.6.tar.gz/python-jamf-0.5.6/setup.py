import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="python-jamf",
    version="0.5.6",
    author="The University of Utah",
    author_email="mlib-its-mac@lists.utah.edu",
    description="Python wrapper for Jamf Pro API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/univ-of-utah-marriott-library-apple/python-jamf",
    packages=setuptools.find_packages(),
    package_data={'': ['*.json']},
    entry_points={
        'console_scripts': ['jamfconfig=jamf.setconfig:setconfig']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # 4 - Beta
        # 5 - Production/Stable
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
    install_requires=['requests>=2.24.0','keyring>=23.0.0'],
)