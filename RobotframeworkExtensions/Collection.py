# **************************************************************************************************************
#
#  Copyright 2020-2024 Robert Bosch GmbH
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
# XC-HWP/ESW3-Queckenstedt
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
from tabulate import tabulate

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

    @staticmethod
    def get_rf_parameters(casesensitive    = True,
                          skipblankstrings = True,
                          comment          = None,
                          startswith       = None,
                          endswith         = None,
                          startsnotwith    = None,
                          endsnotwith      = None,
                          contains         = None,
                          containsnot      = None,
                          inclregex        = None,
                          exclregex        = None):
        """
This method generates a dump of all Robot Framework parameters in the curret scope (including the global parameters).

The output can be filtered (to limit the dumped parameters to the desired ones).

This method returns a dictionary containing all dumped parameters.

In this module the method ``get_rf_parameters`` is used by the keyword ``get_parameters``. ``get_rf_parameters`` is made a separate static method
to enable also other Python modules to use this method for their own needs.

All input parameters are explained in detail here: `PythonExtensionsCollection.pdf <https://github.com/test-fullautomation/python-extensions-collection/blob/develop/PythonExtensionsCollection/PythonExtensionsCollection.pdf>`_
Section 'String operations with CString', method 'StringFilter'.
        """

        variables = BuiltIn().get_variables()

        list_uppercase     = [] # all letters uppercase
        list_lowercase     = [] # all letters lowercase
        list_capitalized   = [] # first letter uppercase
        list_uncapitalized = [] # first letter lowercase
        list_others        = []
        dict_parameters    = {}
        dict_returned      = {}
        for key, value in variables.items():
            # doing some sorting for better readibility (when dump, group parameters by the way they are typed)
            parameter_name = key # full name including '${', '@{', '&{' and '}'
            if key.startswith('${') or key.startswith('@{') or key.startswith('&{'):
                key = key[2:]
            if key.endswith('}'):
                key = key[:-1]

            if CString.StringFilter(key, casesensitive, skipblankstrings, comment, startswith, endswith, startsnotwith, endsnotwith, contains, containsnot , inclregex , exclregex):
                dict_parameters[key] = {"name" : parameter_name, "value" : value} # keyword intarnal helper
                dict_returned[key] = value # what will be returned from keyword
                if len(key) > 3:
                    if key.isupper():
                        list_uppercase.append(key)
                    elif key.islower():
                        list_lowercase.append(key)
                    elif key[0].isupper():
                        list_capitalized.append(key)
                    elif key[0].islower():
                        list_uncapitalized.append(key)
                    else:
                        list_others.append(key)
                else:
                    list_others.append(key)

        list_uppercase.sort()
        list_lowercase.sort()
        list_capitalized.sort()
        list_uncapitalized.sort()
        # currently no need to sort this list # list_others.sort()

        tuple_valuelists = (list_uppercase, list_lowercase, list_capitalized, list_uncapitalized, list_others)
        max_char = 120

        output_table_rows = []
        for valuelist in tuple_valuelists:
            for param in valuelist:
                str_value = f"{dict_parameters[param]['value']}"
                if len(str_value) > max_char:
                    str_value = str_value[:max_char] + " ..."
                output_table_rows.append([f"{param}", "=", f"{str_value}"])

        # -- convert to table and log
        parameter_table = tabulate(output_table_rows, tablefmt="fancy_grid")
        BuiltIn().log("\n" + parameter_table, level="INFO", html=False, console=False)

        return dict_returned

    # eof def get_rf_parameters

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

    @keyword
    def get_parameters(self, casesensitive = True,
                             startswith    = None,
                             endswith      = None,
                             startsnotwith = None,
                             endsnotwith   = None,
                             contains      = None,
                             containsnot   = None,
                             inclregex     = None,
                             exclregex     = None):
        """
This keyword generates a dump of all Robot Framework parameters in the curret scope (including the global parameters).

The output can be filtered (to limit the dumped parameters to the desired ones).

This keyword returns a dictionary containing all dumped parameters.

All input parameters are explained in detail here: `PythonExtensionsCollection.pdf <https://github.com/test-fullautomation/python-extensions-collection/blob/develop/PythonExtensionsCollection/PythonExtensionsCollection.pdf>`_
Section 'String operations with CString', method 'StringFilter'.
        """

        dict_returned = get_rf_parameters(casesensitive=casesensitive,
                                          skipblankstrings=True, # not really required at keyword level
                                          comment=None,          # not really required at keyword level
                                          startswith=startswith,
                                          endswith=endswith,
                                          startsnotwith=startsnotwith,
                                          endsnotwith=endsnotwith,
                                          contains=contains,
                                          containsnot=containsnot,
                                          inclregex=inclregex,
                                          exclregex=exclregex)
        return dict_returned

    # --------------------------------------------------------------------------------------------------------------

# eof class Collection(object):

