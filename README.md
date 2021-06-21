# Script to find Grandfather'ed NAV for Mutual Funds

### Important: 
- This is a proof of concept project. **Use at your own risk.**
- The data is pulled from AMFI site https://www.amfiindia.com/spages/NAVAll_31Jan2018.txt?t=18062021062831 
- And finally, I know code quality may not be great. Suggestions are welcome. 

### Usage:

Download this code as zip, and extract it to some folder like ```C:\temp\grandfather_nav```. The py files should be in ```C:\temp\grandfather_nav```.
Install all the dependencies with the below. This is a one-time activity (for anyone not familiar with Python)
```
pip install -r requirements.txt
```
Finally, run the script file to get help:
```
python main.py -h
```

To know the grandfather'ed NAV of any mutual fund with known ISIN : 
```
python main.py -i <ISIN>
```

To know the grandfathere'd NAV for specific MF AMC all schemes
```
python main.py -n "Mutual Fund Name"
```

To know the names of all MF AMC
```
python main.py -m
```

To know the names of all MF Scheme types 
```
python main.py -t
```

To just download the AMFI data in a text file 
```
python main.py -d
```
### Notes:



### Python 3.7.x Installation in Windows
- Check if Python is already installed by opening command prompt and running ```python --version```.
- If the above command returns ```Python <some-version-number>``` you're probably good - provided version number is above 3.6
- If Python's not installed, command would say something like: ```'python' is not recognized as an internal or external command, operable program or batch file.```
- If so, download the installer from: https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe
- Run that. In the first screen of installer, there will be an option at the bottom to "Add Python 3.7 to Path". Make sure to select it.
- Open command prompt and run ```python --version```. If everything went well it should say ```Python 3.7.x```
- You're all set! 
