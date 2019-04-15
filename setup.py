from setuptools import setup, find_packages


with open("README.md") as f:
    long_description = f.read()

setup(  
    name = "chadlib",
    version = "0.1.1",
    description = "Common classes between my projects",
    long_description = long_description,
    long_description_content_type='text/markdown',
    author = "Chad Reynolds",
    author_email = "cjreynol13@aol.com",
#    url = "",
#    project_urls = { "Source" : ""
#        },
    license = "MIT",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        ],
    keywords = "gui io",
    python_requires = ">=3",
    packages = find_packages(),
#    test_suite = "tests"
)
