#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from setuptools import setup
from setuptools import find_packages

packages = find_packages()

setup(
    name = "grakn-protocol",
    version = "2.0.0-alpha-11",
    description = "Grakn gRPC Protocol",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers = ["Programming Language :: Python", "Programming Language :: Python :: 3", "Programming Language :: Python :: 3.6", "Programming Language :: Python :: 3.7", "Programming Language :: Python :: 3.8", "Programming Language :: Python :: 3.9", "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)", "Operating System :: OS Independent", "Intended Audience :: Developers", "Intended Audience :: Science/Research", "Environment :: Console", "Topic :: Database :: Front-Ends"],
    keywords = "grakn database graph knowledgebase knowledge-engineering",
    url = "https://github.com/graknlabs/protocol/",
    author = "Grakn Labs",
    author_email = "grabl@grakn.ai",
    license = "AGPLv3+",
    packages=packages,
    install_requires=[],
    zip_safe=False,
)
