del .\logfiles\01.test.pretty_print.log
del .\logfiles\01.test.pretty_print.xml
del .\logfiles\01.test.pretty_print_log.html
del .\logfiles\01.test.pretty_print_report.html
del .\logfiles\PersistentParams.pkl
"%ROBOTPYTHONPATH%/python.exe" -m robot -d ./logfiles -o 01.test.pretty_print.xml -l 01.test.pretty_print_log.html -r 01.test.pretty_print_report.html -b 01.test.pretty_print.log ./01.test.pretty_print.robot
