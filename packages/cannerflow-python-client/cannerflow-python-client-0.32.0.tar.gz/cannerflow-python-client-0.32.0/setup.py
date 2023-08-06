# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
import re
from setuptools import setup
import textwrap
from os import path


_version_re = re.compile(r"__version__\s+=\s+(.*)")


with open("cannerflow/__init__.py", "rb") as f:
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'public_readme.md'), encoding='utf-8') as f:
    long_description = f.read()

kerberos_require = ["requests_kerberos"]

all_require = [kerberos_require]

tests_require = all_require + ["httpretty", "pytest", "pytest-runner"]

py27_require = ["ipaddress", "typing"]

setup(
    name="cannerflow-python-client",
    author="Cannerflow Team",
    author_email="contact@canner.io",
    version=version,
    url="https://github.com/canner/cannerflow-python-client",
    packages=["cannerflow"],
    package_data={"": ["LICENSE", "README.md"]},
    description="Client for the Cannerflow",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Database :: Front-Ends",
    ],
    install_requires=["click", "requests", "six", "pandas", "Pillow", "aiohttp", "nest_asyncio", "pyarrow", "fastparquet", "json_lines"],
    extras_require={
        "all": all_require,
        "kerberos": kerberos_require,
        "tests": tests_require,
        ':python_version=="2.7"': py27_require,
    },
)
