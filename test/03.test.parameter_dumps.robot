#  Copyright 2020-2026 Robert Bosch GmbH
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

*** Settings ***

Documentation    parameter dumps test suite

Metadata    TEST_FILE_METADATA_1    test file metadata 1 value
Metadata    TEST_FILE_METADATA_2    test file metadata 2 value
Metadata    TEST_FILE_METADATA_3    test file metadata 3 value
Metadata    TEST_FILE_METADATA_4    test file metadata 4 value

Resource    ./imports/testimport.resource

Suite Setup      testsuites.testsuite_setup    ./config/ext-test_variants.jsonp
Suite Teardown   testsuites.testsuite_teardown
Test Setup       testsuites.testcase_setup
Test Teardown    testsuites.testcase_teardown

*** Variables ***

@{robot_file_param}    123
...                    456
...                    789

*** Test Cases ***

# **************************************************************************************************************

log_parameter
    [Documentation]    Test of keyword 'log_parameter'

    rf.extensions.log_parameter    ${robot_file_param}    parameter: robot_file_param    parameter headline

log_metadata
    [Documentation]    Test of keyword 'log_metadata'

    rf.extensions.log_metadata

get_parameters
    [Documentation]    Test of keyword 'get_parameters'

    ${test_parameters_1}    rf.extensions.get_parameters    startswith=param
    log_dictionary    ${test_parameters_1}

    ${test_parameters_2}    rf.extensions.get_parameters    contains=bench
    log_dictionary    ${test_parameters_2}

