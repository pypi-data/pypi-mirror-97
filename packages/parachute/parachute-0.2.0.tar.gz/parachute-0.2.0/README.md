Parachute
=========

Parachute is a swiss army knife for ArduPilot settings. It helps you quickly and
easily back up all your parameters to a file (and restore them). It also lets
you get/set them, filter them, diff them, restore them or convert them to
parameter files compatible with Mission Planner/QGroundControl.


Installation
------------

Installing Parachute is simple. You can use `pipx` (recommended):

```
$ pipx install parachute
```

Or `pip` (less recommended):

```
$ pip install parachute
```


Usage
-----

Parachute is called like so:

```
$ parachute backup <craft name>
```

For example:

```
$ parachute backup Mini-Drak
```

To restore:

```
$ parachute restore backup.chute
```


Conversion
----------

You can also convert a Parachute file to a file compatible with Mission Planner or QGroundControl:

```
$ parachute convert qgc Mini-Drak_2021-03-02_02-29.chute Mini-Drak.params
```


Filtering
---------

You can filter parameters based on a regular expression:

```
$ parachute filter "serial[123]_" Mini-Drak_2021-03-02_02-29.chute filtered.chute
```

Since all parameter names are uppercase, the regex is case-insensitive, for convenience.

You can also filter when converting:

```
$ parachute convert --filter=yaw mp Mini-Drak_2021-03-02_02-29.chute -
```


Comparing
---------

You can compare parameters in a backup with parameters on the craft:

```
$ parachute compare backup.chute
```


Getting/setting
---------------

You can get and set parameters:

```
$ parachute get BATT_AMP_OFFSET BATT_AMP_PERVLT
```

```
$ parachute set BATT_AMP_OFFSET=-0.0135 BATT_AMP_PERVLT=63.8826
```
