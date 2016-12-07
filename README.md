# RPI-Incident-Map [![Build Status](https://travis-ci.org/sschatts/RPI-Incident-Map.svg?branch=master)](https://travis-ci.org/sschatts/RPI-Incident-Map)
A map that displays the locations and details of various incidents reported to public safety on and around the RPI campus. The information for these incident pins is parsed from the [RPI's Public Safety Daily Crime Log](http://rpi.edu/dept/public_safety/campus/index.html). 

RPI Incident Map is hosted on [AWS](http://rpiincidentmap.com/). 

## Getting Started
### Requirements
- [Python](https://www.python.org/) version 2.7
- [Pymongo](https://api.mongodb.com/python/current/installation.html)
- [Mapbox](https://www.mapbox.com/)
- [pytest](http://doc.pytest.org/en/latest/)
- [Geocoder](https://www.mapbox.com/geocoding/)
- [lxml](http://lxml.de/)
- [Git](https://git-scm.com/)
- [mongoDB](https://www.mongodb.com/)

## Features
- Displaying the pins on the map based on the location they occurred.
- Selecting functionality based on location, type of incident or month they occured.
- Able to zoom and move functionality on the map.
- Contact information available for RPI Public Safety.

## Automated Testing
Use Travis CI for our testing. Repo gets tested on every build.

## Coding Standards
1. We are using tabs instead of spaces to ensure we are staying consistent across the different files in the repository.
2. In out text editors we have declared tabs are equivalent to four spaces because different text editors vary the number of spaces that are equivalent to one tab.
3. We use uppercamelcase for all classes and variables to improve readability and maintain consistency in all files.
4. All private variables begin with __, which is a coding standard for Python.
5. All code is commented with functionality explanation so that returning to old code is easy and new developers understand the purpose of each of the functions.
6. We use double quotes for strings.
7. We add spaces between operators (i.e. x = y instead of x=y).


Developed by:
[Sarah Schattschneider](https://github.com/sschatts), [Christina Hammer](https://github.com/christina-hammer), [Levin Huang](https://github.com/huangl6) and [Edward McCorry](https://github.com/mccore)



