# MLX90641 driver for device tree on a SBC.

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/melexis-fir/mlx90641-driver-devicetree-py?label=github-latest-release-tag)](https://github.com/melexis-fir/mlx90641-driver-devicetree-py/releases) [![GitHub Workflow Status](https://github.com/melexis-fir/mlx90641-driver-devicetree-py/workflows/build-test-publish/badge.svg)](https://github.com/melexis-fir/mlx90641-driver-devicetree-py/actions?query=event%3Arelease) ![Lines of code](https://img.shields.io/tokei/lines/github/melexis-fir/mlx90641-driver-devicetree-py)  

[![PyPI](https://img.shields.io/pypi/v/mlx90641-driver-devicetree)](https://pypi.org/project/mlx90641-driver-devicetree) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mlx90641-driver-devicetree) ![PyPI - License](https://img.shields.io/pypi/l/mlx90641-driver-devicetree)  

![platform](https://img.shields.io/badge/platform-linux%20PC%20%7C%20rasberry%20pi%204%20%7C%20Jetson%20Nano%20%7C%20beagle%20bone-lightgrey)  

MLX90641 is a thermal camera (16x12 pixels) using Far InfraRed radiation from objects to measure the object temperature.  
https://www.melexis.com/mlx90641  
The python package "[mlx90641-driver](https://github.com/melexis-fir/mlx90641-driver-py)" driver interfaces the MLX90641 and aims to facilitate rapid prototyping.

This package provide the I2C low level routines.
It uses the I2C from the device tree of a single board computer(SBC).  

## Getting started

### Installation

```bash
pip install mlx90641-driver-devicetree
```

https://pypi.org/project/mlx90641-driver-devicetree  
https://pypistats.org/packages/mlx90641-driver-devicetree

__Note:__  
Make sure the user has access to `/dev/i2c-<x>`.  
And easy way to do this is by adding the user to the group `i2c`.

### Running the driver demo

* Connect the MLX90641 on the I2C bus of the SBC.  
* Open a terminal and run following command:  

```bash
mlx90641-dump-devicetree /dev/i2c-1
```

This program takes 1 optional argument.

```bash
mlx90641-dump-devicetree <communication-port>
```

Note: this dump command is not yet available!
