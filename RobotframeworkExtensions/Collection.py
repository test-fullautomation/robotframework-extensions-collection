#  Copyright 2020-2022 Robert Bosch GmbH
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

"""
The Collection module is the interface between the Python Extensions Collection and the Robotframework.

This library containing the keyword definitions, can be imported in the following way:

.. code::

   Library    RobotframeworkExtensions.Collection    WITH NAME    rf.extensions

"""

# -- import standard Python modules
import pickle, os, time, random

# -- import Robotframework API
from robot.api.deco import keyword, library # required when using @keyword, @library decorators
from robot.libraries.BuiltIn import BuiltIn

# -- import own Python modules
from PythonExtensionsCollection.Utils.CUtils import *
from PythonExtensionsCollection.String.CString import CString

from RobotframeworkExtensions.version import VERSION
from RobotframeworkExtensions.version import DATE

# --------------------------------------------------------------------------------------------------------------

sThisModuleName    = "Collection.py"
sThisModuleVersion = VERSION
sThisModuleDate    = DATE
sThisModule        = sThisModuleName + " v. " + sThisModuleVersion + " / " + sThisModuleDate

# --------------------------------------------------------------------------------------------------------------
# 
@library
class Collection(object):
    """Module main class
    """

    ROBOT_AUTO_KEYWORDS   = False # only decorated methods are keywords
    ROBOT_LIBRARY_VERSION = sThisModuleVersion
    ROBOT_LIBRARY_SCOPE   = 'GLOBAL'

    # --------------------------------------------------------------------------------------------------------------
    #TM***

    def __init__(self, sThisModule=sThisModule):
        self.sThisModule = sThisModule # in case of debugging

    def __del__(self):
        pass

    # --------------------------------------------------------------------------------------------------------------
    #TM***
    
    @keyword
    def pretty_print(self, oData=None):
       """
The ``pretty_print`` keyword logs the content of parameters of any Python data type (input: ``oData``).

Simple data types are logged directly. Composite data types are resolved before logging.

The output contains for every parameter: the value, the type and counter values (in case of composite data types).

The trace level for output is ``INFO``.

The output is also returned as list of strings.

**Arguments:**

* ``oData``

  / *Condition*: required / *Type*: any Python type /

  Data to be pretty printed

**Returns:**

* ``listOutLines`` (*list*)

  / *Type*: list /

  List of strings containing the resolved data structure of ``oData`` (same content as printed to console).


**Example:**

Variable of Python type ``list``:

.. code::

   set_test_variable    @{aItems}    String
   ...                               ${25}
   ...                               ${True}
   ...                               ${None}

Call of ``pretty_print`` keyword:

.. code::

   rf.extensions.pretty_print    ${aItems}

Output:

.. code::

   INFO - [LIST] (4/1) > [STR]  :  'String'
   INFO - [LIST] (4/2) > [INT]  :  25
   INFO - [LIST] (4/3) > [BOOL]  :  True
   INFO - [LIST] (4/4) > [NONE]  :  None
       """

       # BuiltIn().log(f"This is {self.sThisModule}", "INFO") # debug

       oTypePrint   = CTypePrint()
       listOutLines = oTypePrint.TypePrint(oData)
       for sLine in listOutLines:
          BuiltIn().log(sLine, "INFO")

       return listOutLines

    # eof pretty_print(self, oData=None):

    # --------------------------------------------------------------------------------------------------------------
    #TM***

    @keyword
    def normalize_path(self, sPath=None, bWin=False, sReferencePathAbs=None, bConsiderBlanks=False, bExpandEnvVars=True, bMask=True):
       """
The ``normalize_path`` keyword normalizes local paths, paths to local network resources and internet addresses

**Arguments:**

* ``sPath``

  / *Condition*: required / *Type*: str /

  The path to be normalized

* ``bWin``

  / *Condition*: optional / *Type*: bool / *Default*: False /

  If ``True`` then the returned path contains masked backslashes as separator, otherwise slashes

* ``sReferencePathAbs``

  / *Condition*: optional / *Type*: str / *Default*: None /

  In case of ``sPath`` is relative and ``sReferencePathAbs`` (expected to be absolute) is given, then
  the returned absolute path is a join of both input paths

* ``bConsiderBlanks``

  / *Condition*: optional / *Type*: bool / *Default*: False /

  If ``True`` then the returned path is encapsulated in quotes - in case of the path contains blanks

* ``bExpandEnvVars``

  / *Condition*: optional / *Type*: bool / *Default*: True /

  If ``True`` then in the returned path environment variables are resolved, otherwise not.

* ``bMask``

  / *Condition*: optional / *Type*: bool / *Default*: True (requires ``bWin=True``) /

  If ``bWin`` is ``True`` and ``bMask`` is ``True`` then the returned path contains masked backslashes as separator.

  If ``bWin`` is ``True`` and ``bMask`` is ``False`` then the returned path contains single backslashes only - this might be
  required for applications, that are not able to handle masked backslashes.

  In case of ``bWin`` is ``False`` ``bMask`` has no effect.

**Returns:**

* ``sPath``

  / *Type*: str /

  The normalized path (is ``None`` in case of ``sPath`` is ``None``)


**Example 1:**

Variable containing a path with:

* different types of path separators
* redundant path separators (but backslashes have to be masked in the definition of the variable, this is *not* an unwanted redundancy)
* up-level references

.. code::

   set_test_variable    ${sPath}    C:\\\\subfolder1///../subfolder2\\\\\\\\../subfolder3\\\\

Printing the content of ``sPath`` shows how the path looks like when the masking of the backslashes is resolved:

.. code::

   C:\\subfolder1///../subfolder2\\\\../subfolder3\\


Usage of the ``normalize_path`` keyword:

.. code::

   ${sPath}    rf.extensions.normalize_path    ${sPath}

Result (content of ``sPath``):

.. code::

   C:/subfolder3

In case we need the Windows version (with masked backslashes instead of slashes):

.. code::

   ${sPath}    rf.extensions.normalize_path    ${sPath}    bWin=${True}

Result (content of ``sPath``):

.. code::

   C:\\\\subfolder3

The masking of backslashes can be deactivated:

.. code::

   ${sPath}    rf.extensions.normalize_path    ${sPath}    bWin=${True}    bMask=${False}

Result (content of ``sPath``):

.. code::

   C:\\subfolder3

**Example 2:**

Variable containing a path of a local network resource:

.. code::

   set_test_variable    ${sPath}    \\\\\\\\anyserver.com\\\\part1//part2\\\\\\\\part3/part4

Result of normalization:

.. code::

   //anyserver.com/part1/part2/part3/part4

**Example 3:**

Variable containing an internet address:

.. code::

   set_test_variable    ${sPath}    http:\\\\\\\\anyserver.com\\\\part1//part2\\\\\\\\part3/part4

Result of normalization:

.. code::

   http://anyserver.com/part1/part2/part3/part4
       """
       sPath = CString.NormalizePath(sPath, bWin, sReferencePathAbs, bConsiderBlanks, bExpandEnvVars, bMask)
       return sPath

    # --------------------------------------------------------------------------------------------------------------

# eof class Collection(object):

