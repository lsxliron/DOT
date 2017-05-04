# DOT Project Server & CLI

## Installation
1. Create a virtual environment using ```virtualenv```.
2. Activate the new environment.
3. Install dependencies by executing ```pip install -r requirements.txt```

### Prerequisites:
Edit the file ```createDb.py``` and set the ```imgPath``` variable to the images path on your machine.
The script will generate ```DOT.db``` file. that will be used in both the server and the CLI.
In order to use the server please copy the file to ```app/db```.

### CLI
To use the CLI, navigate to ```scripts``` directory and run: 
```
python dot.py --help

usage: dot.py [-h] [--startDate mm-dd-yyyy] [--endDate mm-dd-yyyy]
              [--startTime hh:mm:ss] [--endTime hh:mm:ss] [--rain 0/1]
              [--location loc_id] [--limit int]
              {query,get}

Queries DOT database.

positional arguments:
  {query,get}           query or get

optional arguments:
  -h, --help            show this help message and exit
  --startDate mm-dd-yyyy
                        Start date
  --endDate mm-dd-yyyy  End date
  --startTime hh:mm:ss  Start time
  --endTime hh:mm:ss    End time
  --rain 0/1            Rain status: 0=not-rainy, 1=rainy
  --location loc_id     The locaion ID of the camera
  --limit int           Max. number of results
```

- The first argument of the CLI can ```query``` or ```get```:
    - query - used as a regular SQL statement and prints the results to the STDOUT in a table form.
    - get - downloads the images that were part of the query to ```scripts/img``` directory.
- ```startDate``` and ```endDate``` specify the starting date and ending date of the query. Both of them in the format ```MM-DD-YYYY```
- ```startTime``` and ```endTime``` specify the starting time and ending time of the query. Both of them in the format ```HH:MM:SS```
- ```rain``` - When this argument is not specified, the result will consist of rainy and non-rainy days. Set ```rain``` to ```1``` for rainy days only and ```0``` for non-rainy days only.
- ```location``` - specify the camera location. This argument is an integer.
- ```limit``` - limits the number of results to a specified integer.

####Example:
```
python dot.py query --startDate 01-01-2015 --endDate 12-31-2015 --startTime 00:00:00 --endTime 23:59:59 --limit 100
```

The above example will query the first 100 images of rainy days in 2015 from any location.

##Server
Navigate to the root folder and run ```python runserver.py```.
The server is running in ```http://localhost:5000```
To change the port and ip address, please edit the ```runserver.py``` file.

