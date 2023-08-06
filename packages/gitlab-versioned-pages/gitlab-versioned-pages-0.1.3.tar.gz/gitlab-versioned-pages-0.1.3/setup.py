from setuptools import find_packages, setup


def read_file(file):
    with open(file) as fin:
        return fin.read()


setup(
    name="gitlab-versioned-pages",
    version="0.1.3",
    description="Include documentation for multiple project versions in a single GitLab page",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    author="Alexey Strokach",
    author_email="alex.strokach@utoronto.ca",
    url="https://gitlab.com/ostrokach/gitlab-versioned-pages",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"gitlab_versioned_pages": ["static/*", "templates/*"]},
    install_requires=[
        "jinja2",
        "python-gitlab",
    ],
    include_package_data=True,
    zip_safe=False,
    keywords="gitlab_versioned_pages",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    test_suite="tests",
)
