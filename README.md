![Definition](https://github.com/naujan/memento-mori/blob/master/res/mementomori-dict.png)

# *memento mori*

*memento mori* is a command-line tool, for calculating and displaying expected life length, based on given data. It is a cool way to gain motivation, or to satisfy curiosity.

> **Note:** Provided results are approximate and for *fun* purposes only. They are based on randomized calculations, and do not constitute medical advice. Do not rely on them.

## Description

When executed for the first time, it gathers some data through asking questions, to later approximate the expected life length. The anwsers are used **only for the calculation process**, the data file contains the calculated date, that acts as a reference for the output.

## Features

- Live length approximation based on given data
- 3 output modes:
- - `date` - prints the expected death date and exits
- - `timer` - live clock in format HH:MM:SS
- - `timer-extended` - live clock, showing years, months, days, hours, minutes and seconds.

## Configuration

The default configuration file is initially generated to `~/.config/memento-mori/config.conf`, and contains the mode of the output:

| Mode | Example output |
| :-------- | :------- |
| `date` | `2100-01-21` |
| `timer` | `655120:25:10` |
| `timer-extended` | `70 years, 3 months, 25 days, 2 hours, 24 minutes and 10 seconds left.`

The outputted mode can also be altered using the `-m <mode>` argument.

## Requirements

- [PyYaml](https://pypi.org/project/PyYAML/)
- [python-dateutil](https://pypi.org/project/python-dateutil/)

## Installation

#### Manual download:
```bash
git clone https://github.com/naujan/mementomori.git
cd mementomori
chmod +x install.sh
sudo ./install.sh
```

## TODO

- **Output formatting** - Custom output per mode in configuration
- **Better and better calculations** - Estimations closer to statistics

## License
[MIT License](https://choosealicense.com/licenses/mit/)