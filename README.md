# QNAP Fan Control

This is a python script for manually regulating the QNAP fans, in particular it enables the ability to use setting 0 which is the lowest RPM setting. 

In the QNAP nas I used to have, this setting was not used and the fans always span at ~6,000rpm setting 1. ~3,500 is setting 0.

## Installation

Install Python 3 on the QNAP NAS

Checkout the ```control.py``` and ```settings.ini``` files onto the file system in your desired location

## Usage

Call the script after customizing the ```settings.ini```

```bash
python3 control.py
```

Then create a cronjob to call it with your chosen frequency

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)