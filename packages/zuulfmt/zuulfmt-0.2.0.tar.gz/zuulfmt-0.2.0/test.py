# Copyright (c) 2020 Red Hat
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest
import zuulfmt

samples = [("""
- copy:
    src: file
    dst: new-file
  name: copy a file
  when: true
- command: test
  name: run a command
""", """
- name: copy a file
  when: true
  copy:
    src: file
    dst: new-file

- name: run a command
  command: test
"""), ("""
- job:
    branches:
      - master
      - f33
      - f32
      - epel8
    description: Check the project has a tests/tests.yml
    name: check-for-tests
    nodeset:
      nodes: []
    run: playbooks/rpm/check-for-tests.yaml
- job:
    abstract: true
    description: Base job for RPM build on Fedora Koji
    name: common-koji-rpm-build
    nodeset: fedora-33-container
    protected: true
    provides:
      - repo
    roles:
      - zuul: zuul-distro-jobs
    run: playbooks/koji/build-ng.yaml
    secrets:
      - name: krb_keytab
        secret: krb_keytab
    timeout: 21600
""", """
- job:
    name: check-for-tests
    description: Check the project has a tests/tests.yml
    run: playbooks/rpm/check-for-tests.yaml
    branches:
      - master
      - f33
      - f32
      - epel8
    nodeset:
      nodes: []

- job:
    name: common-koji-rpm-build
    description: Base job for RPM build on Fedora Koji
    run: playbooks/koji/build-ng.yaml
    abstract: true
    nodeset: fedora-33-container
    protected: true
    provides:
      - repo
    roles:
      - zuul: zuul-distro-jobs
    secrets:
      - name: krb_keytab
        secret: krb_keytab
    timeout: 21600
""")]


def fmt(inp, expected):
    got = zuulfmt.fmt(inp)
    if got != expected:
        print("Got: [" + got + "], wanted: [" + expected + "]")
        return False
    return True


def test_samples():
    assert all([fmt(inp, expected) for inp, expected in samples])


if __name__ == '__main__':
    unittest.main()
