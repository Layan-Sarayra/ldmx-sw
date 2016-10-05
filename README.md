# ldmx-sw

The *ldmx-sw* github repository contains a C++ software framework for the proposed [Light Dark Matter Experiment (LDMX)](https://confluence.slac.stanford.edu/display/MME/Light+Dark+Matter+Experiment) based at [SLAC](https://slac.stanford.edu)).

Currently it includes the following modules:

- [Event](https://github.com/LDMXAnalysis/ldmx-sw/tree/master/Event) - Event model classes and ROOT IO implementation
- [SimApplication](https://github.com/LDMXAnalysis/ldmx-sw/tree/master/SimApplication) - Geant4 simulation application with GDML input and ROOT output
- [Detectors](https://github.com/LDMXAnalysis/ldmx-sw/tree/master/Detectors) - GDML detector data files
- [DetDescr](https://github.com/LDMXAnalysis/ldmx-sw/tree/master/DetDescr) - Detector description utilities including detector ID encoding and decoding

The main program created from building this framework is a simulation application which reads a [GDML](http://gdml.web.cern.ch/GDML/) detector description and writes out a [ROOT](https://root.cern.ch) file containing the simulated hits and particles.  The output file can be loaded into the ROOT environment for analysis.

## Prerequisites

You will need the following build tools available in your environment before beginning the installation.

### Linux

At this time, the software has been built and tested only on Linux, specifically a CentOS7 virtual machine.  Older Linux releases such as RHEL6 or SLC6 will likely not work due to various issues.  (ROOT6 installation does not seem to work with the RHEL devtoolset developer kits, unfortunately.)

### CMake

You should have at least CMake 3.0 installed on your machine, and preferably a current version from the [CMake website](https://cmake.org).  As of this writing, the current CMake version is the 3.6.2 release.  The installation will not work with any 2.x version of cmake, which is too old.

### GCC

You will need a version of GCC that supports the C++-11 standard.  I believe that ROOT6 is not compatible with GCC 5 so a 4.7 or 4.8 release is preferrable.  The default compiler on CentOS7 or RHEL7 should suffice.

## External Packages

You will first need to install or have available at your site a number of external dependencies before building the actual framework.

## Xerces

The [Xerces C++](http://xerces.apache.org/xerces-c/download.cgi) framework is required for GDML support in Geant4 so it must be installed first.

You can install it from scratch using a series of commands such as the following:

``` bash
wget http://download.nextag.com/apache/xerces/c/3/sources/xerces-c-3.1.4.tar.gz
tar -zxvf xerces-c-3.1.4.tar.gz
cd xerces-c-3.1.4
./configure --prefix=$PWD
make install
export XERCESDIR=$PWD
```

The environment variable is optional and for convenience.  Where you see these types of variables in these instructions, you may also substitute in explicitly the path to your local installation.

## Geant4

You need to have a local Geant4 installation available with GDML enabled.  You can check for this by looking for the header files in the Geant4 include dir, e.g. by doing `ls G4GDML*.hh` from that directory.  If no files are found, then it is not enabled in your installation.

Assuming you have [downloaded a Geant4 tarball](http://geant4.web.cern.ch/geant4/support/download.shtml), the installation procedure is like the following:

``` bash
tar -zxvf geant4.10.02.p02.tar.gz
cd geant4.10.02.p02
mkdir build; cd build
cmake -DGEANT4_USE_GDML=ON -DGEANT4_INSTALL_DATA=ON -DXERCESC_ROOT_DIR=$XERCESDIR -DGEANT4_USE_OPENGL_X11=ON -DCMAKE_INSTALL_PREFIX=../../geant4.10.02.p02-install ..
make install
export G4DIR=$PWD
```

If you get errors about Xerces not being found, then check that the path you provided is correct and that the directory contains a lib dir with the Xerces so (shared library) files.

Due to a quirk in the Geant4 build system, you should use the "build" rather than "install" directory when specifying this directory later (it will actually use the files from your installation directory which are pointed to from the build area).

## ROOT

LDMX is standardizing on ROOT 6, and no support for ROOT 5 is planned.

ROOT has many installation options and optional dependencies, and the [building ROOT documentation](https://root.cern.ch/building-root) covers this in full detail.

These commands should install a current version of ROOT locally:

``` bash
wget https://root.cern.ch/download/root_v6.06.08.source.tar.gz
tar -zxvf root_v6.06.08.source.tar.gz
mkdir root-6.06.08-build
cd root-6.06.08-build
cmake -Dgdml=ON ../root-6.06.08
make 
export ROOTDIR=$PWD
```

Depending on what extra tools you want to use in ROOT, you should supply your own extra CMake arguments to enable them.

## Building ldmx-sw

Now that Geant4 is installed with GDML support along with ROOT, you should be able to compile the LDMX software framework.

These commands should install the software locally:

``` bash
git clone https://github.com/LDMXAnalysis/ldmx-sw.git
cd ldmx-sw
mkdir build; cd build
cmake -DGeant4_DIR=$G4DIR -DROOT_DIR=$ROOTDIR -DCMAKE_INSTALL_PREFIX=../ldmx-sw-install ..
make install
```

Now you should have an installation of *ldmx-sw* in the *ldmx-sw-install* directory.

## Setting Up the Environment 

There is not yet an automatically generated script which will setup the environment for running the binaries.

I have a local setup script to do this for the software environment at SLAC on NFS:

``` bash
# set some dir variables
basedir=$PWD
swdir=/nfs/slac/g/ldmx/software

# setup Geant4 environment using its supplied shell script
. $swdir/geant4/geant4.10.02.p02-install/bin/geant4.sh

# set the load library path to find external libraries
export LD_LIBRARY_PATH=$swdir/geant4/geant4.10.02.p02-install/lib64:$swdir/xerces/xerces-c-3.1.4/lib:$swdir/root/root-6.06.08-build/lib

# set the load library path for finding the installed LDMX software libraries
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$basedir/ldmx-sw-install/lib

export MALLOC_CHECK_=0
```

The details of how this is setup will depend on your local environment but the above should give some idea of how to do it.  (Eventually there will be a CMake generated script for setting this environment up automatically so this will not be necessary.)

## Running LDMX Programs

There is currently one main binary program created by the framework which is the LDMX Simulation Application.

It can be run from the command line in interactive mode using the `ldmx-sim` command or by supplying a macro like `ldmx-sim run.mac`.

A sample macro might include the following text:

```
/persistency/gdml/read detector.gdml
/run/initialize
/gun/particle e-
/gun/energy 4 GeV
/gun/position -27.926 5 -700 mm
/gun/direction 0.3138 0 3.9877 GeV
/run/beamOn 1000
```

The detector file is located in the *Detectors* module data directory and the easiest way to access this currently is probably by setting some sym links in your current directory e.g. `ln -s ldmx-sw/Detectors/data/ldmx-det-full-v0/*.gdml .`, and then the program should be able to find all the detector files.

## Contributing

To contribute code to the project, you will need to create an account on [github](https://github.com/) if you don't have one already, and then request to be added to the [LDMXAnalysis](https://github.com/orgs/LDMXAnalysis/) organization.

When adding new code, you should do this on a branch created by a command like `git checkout -b johndoe-dev` in order to make sure you don't apply changes directly to the master (replace "johndoe" with your user name).

Then you would `git add` and `git commit` your changes to this branch.

You can then merge in these changes to the local master by doing `git checkout master` and then `git merge johndoe-dev` which will apply your branch updates.

If you don't already have SSH keys configured, you can set this up as follows:

1. [Generate a new SSH key pair](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/).
2. Add the new SSH key to your github account under settings in the [SSH and GPG keys](https://github.com/settings/keys) tab.
3. Add the key to your SSH config file.

My *~/.ssh/config* file looks like this:

```
Host github.com
  Hostname github.com
  User git
  IdentityFile ~/.ssh/id_rsa_github
  PreferredAuthentications publickey
```

Now you can push changes to the master using the command `git push git@github.com:LDMXAnalysis/ldmx-sw.git` without needing to type your user name or password. 

Eventually we will use [pull requests](https://help.github.com/articles/creating-a-pull-request/) for merging in changes from branches to master, but for now committing directly to the master is acceptable.

## Help

Comments, suggestions or cries for help can be sent to [Jeremy McCormick](mailto:jeremym@slac.stanford.edu) or posted in the [#simulation channel](https://ldmxsoftware.slack.com/messages/simulation/) of the [LDMX Software Slack](https://ldmxsoftware.slack.com/).  

If you plan on starting a major (sub)project within the repository like adding a new code module, you should give advance notice and explain your plains beforehand.  :)

## References

* [LDMX Simulation Framework](https://www.dropbox.com/s/oosmuyo553kvlce/LDMX%20Simulation%20Framework.pptx?dl=0) - Powerpoint presentation
