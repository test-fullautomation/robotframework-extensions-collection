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

Documentation    pretty_print test suite
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

PrettyPrintTest_1
    [Documentation]    Test 1 of keyword 'pretty_print': list

    set_test_variable    @{aItems}    TestString
    ...                               ${25}
    ...                               ${True}
    ...                               ${None}

    set_test_variable    @{aItemsExpected}    [LIST] (4/1) > [STR]\ \ :\ \ 'TestString'
    ...                                       [LIST] (4/2) > [INT]\ \ :\ \ 25
    ...                                       [LIST] (4/3) > [BOOL]\ \ :\ \ True
    ...                                       [LIST] (4/4) > [NONE]\ \ :\ \ None

    ${aOutput}    rf.extensions.pretty_print    ${aItems}

    set_test_variable    ${nIndex}    ${0}
    FOR    ${sOutput}    IN    @{aOutput}
        log    ** Output\ \ \ : ${sOutput}    console=yes
        log    ** Expected\ : ${aItemsExpected}[${nIndex}]    console=yes
        should_be_equal    ${sOutput}    ${aItemsExpected}[${nIndex}]
        ${nIndex}    Evaluate    ${nIndex} + 1
    END

# **************************************************************************************************************

# !!! This test needs to be discussed because the type of dItems is not 'dict' or 'dotdict' - like expected,
#     but '<class 'robot.utils.dotdict.DotDict'>'.
#     Therefore CUtils from python-extensions-collection needs to be adapted.
#     With this adaption the test works.
#     Why does the Robotframework not support the same short name 'dotdict' like Python is doing?

PrettyPrintTest_2
    [Documentation]    Test 2 of keyword 'pretty_print' : dict

    set_test_variable    &{dItems}    kVal_1=Val_1
    ...                               kVal_2=Val_2
    ...                               kVal_3=Val_3

    set_test_variable    @{aItemsExpected}    [DOTDICT] (3/1) > {kVal_1} [STR]\ \ :\ \ 'Val_1'
    ...                                       [DOTDICT] (3/2) > {kVal_2} [STR]\ \ :\ \ 'Val_2'
    ...                                       [DOTDICT] (3/3) > {kVal_3} [STR]\ \ :\ \ 'Val_3'

    ${aOutput}    rf.extensions.pretty_print    ${dItems}

    # debug:
    # log    === aOutput : ${aOutput}    console=yes
    # FOR    ${sKey}    IN    @{dItems}
    #     log    * Key : ${sKey} = ${dItems}[${sKey}]    console=yes
    # END

    set_test_variable    ${nIndex}    ${0}
    FOR    ${sOutput}    IN    @{aOutput}
        log    ** Output\ \ \ : ${sOutput}    console=yes
        log    ** Expected\ : ${aItemsExpected}[${nIndex}]    console=yes
        should_be_equal    ${sOutput}    ${aItemsExpected}[${nIndex}]
        ${nIndex}    Evaluate    ${nIndex} + 1
    END

