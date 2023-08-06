# HallgrimJS - an ILIAS task generator in Python

This project was forked form another project called **Hallgrim** created by Jan Maximilian Michal. 
The repository to Hallgrim can be found [here](https://gitlab.gwdg.de/j.michal/ilias-generator).
The difference between the original and HallgrimJS is the addition of a new question type, which allows the use of JavaScript in tasks.

### Installation

To install HallgrimJS download the zip [file](https://user.informatik.uni-goettingen.de/~lukas.mayer/hallgrimJS/hallgrimJS-0.4.0.zip).
Unpack the file and run the following command (**Note:** HallgrimJS *does not* work with Python 2. The command *only* works with Linux):

```
sudo python setup.py install
```

### Usage

After the install just invoke `hallgrimJS -h` to see usage. The directory hallgrimJS
is invoked in, should contain a `config.ini`.

Example scripts from Jan Maximilian Michal can be found
[in a seperate repository](https://gitlab.gwdg.de/j.michal/ilias-scripts).
Two JavaScript example scripts can be found [here](https://user.informatik.uni-goettingen.de/~lukas.mayer/).

### Documentation

Please see the documentation. All the functionality is explained there among
with some code documentation. It was generated with Sphinx. Its output can be found
[here](http://user.informatik.uni-goettingen.de/~lukas.mayer/hallgrimJS/index.html).
This documentation doesn't differ much from the [documenation of Hallgrim](https://user.informatik.uni-goettingen.de/~j.michal/hallgrim/index.html),
except for the addition of the JavaScript question type.


### Notes

The final data is produced in three steps:

1. A python script file with predefined structure that has to export certain
   variables in a specified format.
2. An intermediate representation (probably an array that contains relevant
   data and assumes unknown properties)
3. The XML structure for one or multiple questions, readable by Ilias.
4. An Ilias object packed as .zip file, ready for upload.

### Testing

The tool will ship with a VirtualBox containing Ilias Versions used in
production. With `hallgrimJS upload <xml script>` it is possible to upload these
scripts quickly and see a how they look like in a working Ilias system.
(**Note:** the upload function is currently not working.)
