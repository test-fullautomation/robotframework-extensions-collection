#  Copyright 2020-2022 Robert Bosch Car Multimedia GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////
#
# Copyright (c) 2021 Robert Bosch Car Multimedia GmbH, Hildesheim
#
# Copyright notice:
# This software is property of Robert Bosch Car Multimedia GmbH
# Unauthorized duplication and disclosure to third parties is forbidden.
#
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////

*** Settings ***

Documentation    normalize_path test suite
...    A full unittest of the underlying Python implementation of this keyword is implemented also in Python.
...    This test suite only contains some basic tests to ensure that in general it is possible to use this
...    keyword within a robot file.
...    A certain configuration is not required.

Resource    ./imports/testimport.resource

Suite Setup      testsuites.testsuite_setup
Suite Teardown   testsuites.testsuite_teardown
Test Setup       testsuites.testcase_setup
Test Teardown    testsuites.testcase_teardown

*** Variables ***

*** Test Cases ***

# **************************************************************************************************************

NormalizePathTest_1
    [Documentation]    Test 1 of keyword 'normalize_path'

    ${system}=    Evaluate    platform.system()    platform

    rf.extensions.pretty_print    ${system}

    log    >>>>>>>>>> Test is running under: ${system}

    set_test_variable    ${sPath}    Path: (not supported OS: ${system})
    set_test_variable    ${sPathExpected}    Path expected: (not supported OS: ${system})

    IF    "${system}" == "Windows"
       set_test_variable    ${sPath}    C:\\subfolder1///../subfolder2\\\\../subfolder3\\
       set_test_variable    ${sPathExpected}    C:/subfolder3
    ELSE
       IF    "${system}" == "Linux"
          set_test_variable    ${sPath}    /tmp//subfolder1///..\\subfolder2\\\\../subfolder3\\
          set_test_variable    ${sPathExpected}    /tmp/subfolder3
       END
    END

    log    >>>>>>>>>> (1) sPath : ${sPath}    console=yes
    ${sPathNormalized}    rf.extensions.normalize_path    ${sPath}
    log    >>>>>>>>>> (1) sPathNormalized: ${sPathNormalized}    console=yes

    should_be_equal    ${sPathNormalized}    ${sPathExpected}


NormalizePathTest_2
    [Documentation]    Test 2 of keyword 'normalize_path'

    set_test_variable    ${sPath}    \\\\anyserver.com\\part1//part2\\\\part3/part4
    set_test_variable    ${sPathExpected}    //anyserver.com/part1/part2/part3/part4

    log    >>>>>>>>>> (2) sPath : ${sPath}    console=yes
    ${sPathNormalized}    rf.extensions.normalize_path    ${sPath}
    log    >>>>>>>>>> (2) sPathNormalized: ${sPathNormalized}    console=yes

    should_be_equal    ${sPathNormalized}    ${sPathExpected}

NormalizePathTest_3
    [Documentation]    Test 3 of keyword 'normalize_path'

    set_test_variable    ${sPath}    http:\\\\anyserver.com\\part1//part2\\\\part3/part4
    set_test_variable    ${sPathExpected}    http://anyserver.com/part1/part2/part3/part4

    log    >>>>>>>>>> (3) sPath : ${sPath}    console=yes
    ${sPathNormalized}    rf.extensions.normalize_path    ${sPath}
    log    >>>>>>>>>> (3) sPathNormalized: ${sPathNormalized}    console=yes

    should_be_equal    ${sPathNormalized}    ${sPathExpected}

# **************************************************************************************************************

