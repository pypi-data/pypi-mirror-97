hein_robots
===========

`hein_robots` is an easy-to-use package that provides a common interface for controlling robots used by the Hein Lab.
Currently the Kinova Gen3 is the only robot supported, with support for the Universal Robots UR3 and the North Robotics
N9 on the roadmap.

Requirements
------------

* Python 3.6+

Installation
------------


1. Download the v2.2.0 Kortex API .whl package (required for controlling the Kinova Gen3):

    * https://artifactory.kinovaapps.com:443/artifactory/generic-public/kortex/API/2.2.0/kortex_api-2.2.0.post31-py3-none-any.whl
    
2. Install the downloaded package with `pip`:

        $ pip install <path to kortex_api-2.2.0.post31-py3-none-any.whl>

3. Install the latest `hein_robots` package with `pip`:

        $ pip install hein_robots

License
-------

This project is licensed under the terms of the MIT license.


