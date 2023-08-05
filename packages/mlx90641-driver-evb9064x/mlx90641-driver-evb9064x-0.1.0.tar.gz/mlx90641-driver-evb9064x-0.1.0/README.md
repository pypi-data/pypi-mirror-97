# MLX90641 driver for EVB90640-41

![GitHub release (latest by date)](https://img.shields.io/github/v/release/melexis-fir/mlx90641-driver-evb9064x-py?label=github-latest-release-tag) ![GitHub Workflow Status (event)](https://img.shields.io/github/workflow/status/melexis-fir/mlx90641-driver-evb9064x-py/build-test-publish?event=release&label=github-workflow) ![Lines of code](https://img.shields.io/tokei/lines/github/melexis-fir/mlx90641-driver-evb9064x-py)  

![PyPI](https://img.shields.io/pypi/v/mlx90641-driver-evb9064x) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mlx90641-driver-evb9064x) ![PyPI - License](https://img.shields.io/pypi/l/mlx90641-driver-evb9064x)  

![platform](https://img.shields.io/badge/platform-Win10%20PC%20%7C%20linux%20PC%20%7C%20rasberry%20pi%204%20%7C%20Jetson%20Nano%20%7C%20beagle%20bone-lightgrey)  

MLX90641 is a thermal camera (16x12 pixels) using Far InfraRed radiation from objects to measure the object temperature.  
https://www.melexis.com/mlx90641  
The python package "[mlx90641-driver](https://github.com/melexis-fir/mlx90641-driver-py)" driver interfaces the MLX90641 and aims to facilitate rapid prototyping.

This package provide the I2C low level routines.
It uses the I2C from the EVB90640-41 which is connected via the USB cable to the computer.  
https://www.melexis.com/en/product/EVB90640-41/  

## Getting started

### Installation


```bash
pip install mlx90641-driver-evb9064x
```

https://pypi.org/project/mlx90641-driver-evb9064x  
https://pypistats.org/packages/mlx90641-driver-evb9064x

__Note:__  
On linux OS, make sure the user has access to the comport  `/dev/ttyUSB<x>` or `/dev/ttyACM<x>`.  
And easy way to do this is by adding the user to the group `dialout`.

### Running the driver demo

* Connect the MLX90641 to the EVB
* Connect the EVB to your PC with the USB cable.  
* Open a terminal and run following command:  

```bash
mlx90641-dump-evb9064x auto
```

This program takes 1 optional argument.

```bash
mlx90641-dump-evb9064x <communication-port>
```

Note: this dump command is not yet available!
