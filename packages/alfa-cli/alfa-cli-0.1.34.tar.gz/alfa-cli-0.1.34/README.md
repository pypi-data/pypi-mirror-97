# alfa-cli

This package provides a command line tool for [ALFA](https://widgetbrain.com/product/).

## Installation

You can directly install alfa-cli using [pip](http://www.pip-installer.org/en/latest/). This will install the alfa-cli package as well as all dependencies.

```sh
$ pip install -U alfa-cli
```

If you already have alfa-cli installed and want to upgrade to the latest version, you can run:

```sh
$ pip install --upgrade alfa-cli
```

## Usage

Once alfa-cli is installed, you can run it with the following template.

```sh
$ alfa [options] <command> <subcommand> [parameters]
```

For more information regarding the usage, you can refer to the provided help information.

```sh
$ alfa --help
$ alfa <command> --help
$ alfa <command> <subcommand> --help
```

## Command Completion

The alfa-cli package includes a command completion feature, but is not automatically installed.
To enable tab completion you can follow the instructions below:

For `bash`, run the following command, or append it to `~/.bashrc`

```sh
$ . alfa-complete.sh
```

For `zsh`, run the following command, or append it to `~/.zshrc`

```sh
$ . alfa-complete.zsh
```

## Development

To install requirements locally:

**1.** Activate local venv

```sh
$ virtualenv venv
$ source venv/bin/activate
```

**2.** Install requirements from setup.py

```sh
$ pip install -e .[dev]
```

To develop alfa-cli alongside alfa-sdk, you can opt to install a local copy of the alfa-sdk instead.

```sh
$ pip install -e /path/to/alfa-sdk-py
```

### Running it locally

You can run the cli directly as a python module.

```sh
$ python alfa_cli [options] <command> <subcommand> [parameters]
```

Alternatively, you can install your local copy of alfa-cli in develop mode, and use it normally.

```sh
$ python setup.py develop
$ alfa [options] <command> <subcommand> [parameters]
```
