# chisel-nbdev
> The goal of this repo is to provide a seamless way to develop Chisel code in a Jupyter Notebook environment.


## Requirements (mac)
- setup some virtualenv (im using python3.8.2)
- ```pip install virtualenv```
- find your python3 binary: ```which python3``` which for me is ```/usr/local/bin/python3```
- create virtualenv: ```python3 -m virtualenv --python=/usr/local/bin/python3 chisel_nb_env```
- activate it: ```source chisel_nb_env/bin/activate```
- install jupyterlab (which includes jupyter notebook): ```pip install jupyterlab```## Requirements (mac)
- setup some virtualenv (im using python3.8.2)
- ```pip install virtualenv```
- find your python3 binary: ```which python3``` which for me is ```/usr/local/bin/python3```
- create virtualenv: ```python3 -m virtualenv --python=/usr/local/bin/python3 chisel_nb_env```
- activate it: ```source chisel_nb_env/bin/activate```
- install jupyterlab (which includes jupyter notebook): ```pip install jupyterlab```

### Setup the Jupyter Scala kernel Almond (https://almond.sh) 
- Borrowed from the Chisel-Bootcamp install guide: https://github.com/freechipsproject/chisel-bootcamp/blob/master/Install.md
- If you experience errors or issues with this section, try running rm -rf ~/.local/share/jupyter/kernels/scala/ first.
- Next, download coursier (our dependency manager) and use it to install almond (our kernel wrapped around Ammonite) (see here for the source for these instructions):
```
curl -L -o coursier https://git.io/coursier-cli && chmod +x coursier
SCALA_VERSION=2.12.10 ALMOND_VERSION=0.9.1
./coursier bootstrap -r jitpack \
    -i user -I user:sh.almond:scala-kernel-api_$SCALA_VERSION:$ALMOND_VERSION \
    sh.almond:scala-kernel_$SCALA_VERSION:$ALMOND_VERSION \
    --sources --default=true \
    -o almond
./almond --install
```
- You can delete coursier and almond files if you so desire.

### Start JupyterLab
- Making sure you are in your virtualenv then run: ```jupyter lab```

### Project Structure
- By default, notebook source files (.ipynb) will live in the ```nbs``` folder.
- Upon running ```notebook2script()``` the notebooks in ```nbs``` will export code to ```.sc``` files in the ```nbdev``` folder. These are auto-generated files that can be imported back into notebooks via Ammonite: For example ```import $file.MyMod, MyMod._``` imports the contents of the file ```MyMod.sc```.

### Testing Notebooks
- Currently can run ```nbdev_test_nbs('MyMod.ipynb')``` to run all of the tests contained in the ```MyMod.ipynb``` notebook. 
- Tests are identified by either omitting any export flags (```//export```) or by including special flags defined in ```settings.ini``` (i.e ```//slowtest``` or ```chiseltest```).

### settings.ini
- Configurations belong in this file.
