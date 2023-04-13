# **************************************************************************************************************
#
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
#
# **************************************************************************************************************
#
# Collection.py
#
# XC-CT/ECA3-Queckenstedt
#
# --------------------------------------------------------------------------------------------------------------
#
# 06.04.2023
#
# --------------------------------------------------------------------------------------------------------------

"""
The Collection module is the interface between the PythonExtensionsCollection and the Robot Framework.

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
from RobotframeworkExtensions.version import VERSION_DATE

# --------------------------------------------------------------------------------------------------------------

sThisModuleName    = "Collection.py"
sThisModuleVersion = VERSION
sThisModuleDate    = VERSION_DATE
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
    def pretty_print(self, oData=None, sPrefix=None):
       """
The ``pretty_print`` keyword logs the content of parameters of any Python data type (input: ``oData``).

Simple data types are logged directly. Composite data types are resolved before.

The output contains for every parameter:

* the type
* the total number of elements inside (e.g. the number of keys inside a dictionary)
* the counter number of the current element
* the value

The trace level for output is ``INFO``.

The output is also returned as list of strings.

**Arguments:**

* ``oData``

  / *Condition*: required / *Type*: any Python type /

  Data to be pretty printed

* ``sPrefix``

  / *Condition*: optional / *Type*: str / *Default*: None /

  If not ``None``, this prefix string is added to every output line.

**Returns:**

* ``listOutLines`` (*list*)

  / *Type*: list /

  List of strings containing the resolved data structure of ``oData`` (same content as printed to console).
       """

       # BuiltIn().log(f"This is {self.sThisModule}", "INFO") # debug

       oTypePrint   = CTypePrint()
       listOutLines = oTypePrint.TypePrint(oData)

       if sPrefix is None:
          for sLine in listOutLines:
             BuiltIn().log(sLine, "INFO")
             BuiltIn().log_to_console(sLine)
          return listOutLines
       else:
          listOutLinesNew = []
          for sLine in listOutLines:
             sLine = f"{sPrefix} : {sLine}"
             BuiltIn().log(sLine, "INFO")
             BuiltIn().log_to_console(sLine)
             listOutLinesNew.append(sLine)
          return listOutLinesNew

    # eof def pretty_print(self, oData=None, sPrefix=None):

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
       """
       sPath = CString.NormalizePath(sPath, bWin, sReferencePathAbs, bConsiderBlanks, bExpandEnvVars, bMask)
       return sPath

    # --------------------------------------------------------------------------------------------------------------

# eof class Collection(object):

