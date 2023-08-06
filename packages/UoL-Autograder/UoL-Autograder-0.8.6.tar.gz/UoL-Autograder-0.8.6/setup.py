from setuptools import setup, find_packages
import os

version = os.environ.get('CI_COMMIT_TAG', None)
version_file = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "feedback/VERSION")

if not version:
    with open(version_file) as f:
        version = f.read()
else:
    with open(version_file, "w") as f:
        f.write(version)
print(version)

dependencies = [
    'pylint',
    'appdirs',
    'psutil'
]

setup(
    name='UoL-Autograder',
    package_dir={
        "feedback": "feedback",
        "feedback.cpp": "feedback/cpp",
        "feedback.general": "feedback/general",
        "feedback.py": "feedback/py",
        "feedback.builder": "feedback/builder"
    },
    packages=["feedback",
              "feedback.cpp",
              "feedback.general",
              "feedback.py",
              "feedback.builder"
              ],
    version=version,
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='ecl-2.0',
    description='General testing and feedback',
    author='Titusz Ban, Craig Evans & Sam Wilson @ Leeds Institute for Teaching Excellence',
    author_email='el16ttb@leeds.ac.uk',
    package_data={
        "": [
            "*.json",
            "*.cpp",
            "*.h",
            "*.hpp",
            "*.sh",
        ]
    },
    include_package_data=True,
    keywords=[],
    install_requires=dependencies,
    setup_requires=dependencies,
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Topic :: Software Development :: Build Tools',
        'License :: Free For Educational Use',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            "feedback=feedback.__main__:main",
            "feedback-builder=feedback.builder.__main__:main"
        ]
    }
)
