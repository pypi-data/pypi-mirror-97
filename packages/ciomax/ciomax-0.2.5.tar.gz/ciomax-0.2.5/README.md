# Conductor for 3DS Max

Max plugin submitter for the Conductor Cloud rendering service.

## Install

**To install the latest version.**
```bash
pip install --upgrade ciomax --target=$HOME/Conductor
```

**To install a specific version, for example 0.1.0.**
```bash
pip install --upgrade --force-reinstall ciomax==0.1.0 --target=$HOME/Conductor
```

**Then setup the Plugin startup file from a windows machine.** 

```bash
python ~/Conductor/ciomax/post_install.py
```

## Usage

To set up a render, go to **Rendering** menu in 3ds Max and choose **Render with Conductor**.

For detailed help, checkout the [tutorial](https://docs.conductortech.com/tutorials/max) and [reference](https://docs.conductortech.com/reference/max) documentation.

## License
[MIT](https://choosealicense.com/licenses/mit)