import setuptools
import os

if __name__ == '__main__':
    # description
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "readme.md"), "r") as fh:
        long_description = fh.read()

    # requirements
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt"), "r") as f:
        requirements = f.read().splitlines()

    setuptools.setup(
        name="polzybackend",
        version="0.7.0",
        author="Bernhard Buhl",
        author_email="buhl@buhl-consulting.com.cy",
        description="Open source Insurance Policy Life Cycle Management",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://baangt.org",
        packages=setuptools.find_packages(),
        data_files=[],
        package_data={},
        install_requires=requirements,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        include_package_data=True,
        python_requires='>=3.6',
    )
