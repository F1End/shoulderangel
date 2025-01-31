# shoulderangel
This is a focusing app. Watches you(r computer) and nudges you if you do something that you should not, as if it were an angel.

![Alt text](/images/sa1.png)

Following a set of configurations will create a popup window if the specified application(s) are running during the specified interval.

For example, if you want to prevent yourself from browsing at night, you can create a configuartion that will trigger popups if you are using Chrome and Firefox between 11 PM and 8 AM.

**Usage**
1. Clone or download the repository
2. Optional: Create a virtual environment
3. Install dependencies.
4. Create config file.
   1. A simple base config is available in config directory as config.yaml
      
   ![Alt text](/images/config_example_1.png)
   
   2. You can create multiple sets, each will be evaluated automatically when the script runs
   3. You can list single or multiple programs(simply comma delimited)
   4. Please add start_time and end_time in form "hh:mm", including double brackets
   5. Currently the only supported rule is nudge, as in the image. This will trigger a popup window with a message in case the progrems are found to be running between start and end times.
   6. You can find further examples in tests/resources directory
6. Create the command to run the script.
   1. The command will start with a reference to your python setup.
      1. If running from virtual environment, it would start as "./venv/Script/python.exe" or comparable
      2. If python is added to your path, simply "python" should work
   2. The file to be run is main.py
   3. The following switches are supported (also printed out if run with --help)
      1. --config_path: this should be followed by a path to your config file. If not given, defaults to /config/config.yaml
      2. --run_rule: if "single", the app will quit after running the check on the content of the config file. If "loop" is used, the app will keep looping and checking/triggering popup until interrupted.
      3. --check_interval: if run rule is loop, this is the time between two checks, given in minutes. E.g. if 0.5 it will check every 30 seconds
   4. Sample commands:
      1. \venv\Scripts\python.exe main.py
      2. D:\PythonProjects\shoulderangel\venv\Scripts\python.exe D:\PythonProjects\shoulderangel\main.py --run_rule loop --config_path C:\Users\JohnDoe\myconfig.yaml
      3. python D:\PythonProjects\shoulderangel\main.py --run_rule loop --config_path --check_interval 2.5
7. Run the script by
   1. Using cmd or powershell line from venv:
   https://www.geeksforgeeks.org/how-to-use-cmd-for-python-in-windows-10/
   2. Using task scheduler:https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10
