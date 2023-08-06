# ITS Private Cloud Python Client ``pyvss``

[![CI][build-img]](https://gitlab-ee.eis.utoronto.ca/vss/py-vss/commits/master)
[![Coverage][coverage-img]](https://gitlab-ee.eis.utoronto.ca/vss/py-vss/commits/master)
[![PyPI][pypi-img]](https://pypi.python.org/pypi/pyvss)
[![PyPI version][pyver-img]](https://pypi.python.org/pypi/pyvss)
[![Docker Image Pulls][docker-pulls-img]][docker-image]
[![Docker Image Layers][docker-layer-img]][docker-image]
[![Docker Image Version][docker-version-img]][docker-image]

   
## Documentation

Package documentation is now available at [docs][docs].

## Installation

The fastest way to install PyVSS is to use [pip][pip]:

```bash
pip install pyvss
```

To interact with `vskey-stor`, install pyvss with extras:

```bash
pip install pyvss[stor]
```

If you have PyVSS installed and want to upgrade to the latest version you can run:

```bash
pip install --upgrade pyvss
```

This will install PyVSS as well as all dependencies. 

You can also just [download the tarball][download the tarball]. Once you have the `py-vss` directory structure on your workstation, you can just run:

```bash
cd <path_to_py-vss>
pip install .
```

### macOS

You can use `pip` directly to install PyVSS. Run `pip --version` to see if your version of
macOS already includes Python and `pip`.

```bash
pip --version
```

> If you don't have `pip` installed, first download and install 
   [Python 3.7 for Mac][Python 3.7 for Mac] from the downloads page of Python.org. 
   Download and run the `pip` installation script provided by the Python Packaging Authority.

       curl -O https://bootstrap.pypa.io/get-pip.py
       python3 get-pip.py --user


1. Use `pip` to install PyVSS.

```bash
pip install pyvss --upgrade --user
```

2. Verify that the PyVSS is installed correctly.

```bash
pip freeze | grep pyvss
```

### Linux

You can use `pip` directly to install PyVSS. Run `pip --version` to see if your version of
Linux already includes Python and `pip`.

```bash
   pip --version
```

>  If you don't have `pip` installed, first download and install 
   [Python 3.5 for Linux][Python 3.5 for Linux] from the
   downloads page of Python.org or using your preferred package manager.
   Download and run the `pip` installation script provided by the Python Packaging Authority.

       curl -O https://bootstrap.pypa.io/get-pip.py
       python3 get-pip.py --user

1. Use `pip` to install PyVSS.

```bash
pip install pyvss --upgrade --user
```

2. Verify that the PyVSS is installed correctly.

```bash
pip freeze | grep pyvss
```

### Windows

1. Open the Command Prompt from the Start menu.

2. Use the following commands to verify that **Python** and `pip` are both installed correctly.

```batch
C:\Windows\System32> python --version
Python 3.7.1
C:\Windows\System32> pip --version
pip 18.1 from c:\program files\python37\lib\site-packages\pip (python 3.7)
```

3. Install PyVSS CLI using pip.

```batch
C:\Windows\System32> pip install pyvss
```

4. Verify that PyVSS is installed correctly.

```batch
C:\Windows\System32> pip freeze | findstr pyvss
```

## Docker

For more information refer to the [Docker](docker/README.md) section.

Use
===

Create an instance of ``VssManager`` passing your **ITS Private Cloud API access token**
and your are all set to start calling any of the self-descriptive methods included:

```python
from pyvss.manager import VssManager
vss = VssManager(tk='api_token')
# list vms
vms = vss.get_vms()
# list folders
folders = vss.get_folders()
# networks
networks = vss.get_networks()
# domains
domains = vss.get_domains()
# power cycle vm
vss.power_cycle_vm(uuid='<uuid>')  
# create vm
req = vss.create_vm(os='ubuntu64Guest', built='os_install',
                    description='Testing python wrapper',
                    folder='group-v6736', bill_dept='EIS', disks=[100, 100])
uuid = vss.wait_for_request(req['_links']['request'], 'vm_uuid', 'Processed')
# creating multiple vms
reqs = vss.create_vms(count=3, name='python', os='ubuntu64Guest', bill_dept='EIS',
        description='Testing multiple deployment from python wrapper',
        folder='group-v6736', built='os_install')
uuids = [vss.wait_for_request(r['_links']['request'], 'vm_uuid', 'Processed') for r in reqs]
# power on recently created vms
for uuid in uuids:
   vss.power_on_vm(uuid)    
# create snapshot
req = vss.create_vm_snapshot(uuid='5012abcb-a9f3-e112-c1ea-de2fa9dab90a',
                             desc='Snapshot description',
                             date_time='2016-08-04 15:30',
                             valid=1)
snap_id = vss.wait_for_request(req['_links']['request'], 'snap_id', 'Processed')
# revert to snapshot
req = vss.revert_vm_snapshot(uuid, snap_id)
```

An alternative is to generate a token from within the ``VssManager`` class and this can be done
by setting the following environment variables

```bash
export VSS_API_USER='username'
export VSS_API_USER_PASS='username_password'
```

Then, from the ``VssManager`` call the ``get_token`` method as follows:

```python
from pyvss.manager import VssManager
vss = VssManager()
vss.get_token()
```   

## Getting Help

We use GitLab issues for tracking bugs, enhancements and feature requests.
If it turns out that you may have found a bug, please [open a new issue][open a new issue].

## Versioning

The API versions are tagged based on [Semantic Versioning](https://semver.org/). Versions available in the 
[tags section](https://gitlab-ee.eis.utoronto.ca/vss/py-vss/tags).

## Contributing

Refer to the [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process of 
submitting code to the repository.

[docs]: https://eis.utoronto.ca/~vss/pyvss/
[download the tarball]: https://pypi.python.org/pypi/pyvss
[Click]: http://click.pocoo.org/6/
[Python Releases for Windows]: https://www.python.org/downloads/windows/
[pip]: http://www.pip-installer.org/en/latest/
[open a new issue]: https://gitlab-ee.eis.utoronto.ca/vss/py-vss/issues/new>
[Alpine Linux]: https://hub.docker.com/_/alpine/
[PyVSS]: https://pypi.python.org/pypi/pyvss
[build-img]: https://gitlab-ee.eis.utoronto.ca/vss/py-vss/badges/master/pipeline.svg
[coverage-img]: https://gitlab-ee.eis.utoronto.ca/vss/py-vss/badges/master/coverage.svg
[pypi-img]: https://img.shields.io/pypi/v/pyvss.svg
[pyver-img]: https://img.shields.io/pypi/pyversions/pyvss.svg
[docker-pulls-img]:  https://img.shields.io/docker/pulls/uofteis/pyvss.svg
[docker-layer-img]: https://images.microbadger.com/badges/image/uofteis/pyvss.svg
[docker-version-img]: https://images.microbadger.com/badges/version/uofteis/pyvss.svg
[docker-image]: https://hub.docker.com/r/uofteis/pyvss/
[Python 3.7 for Mac]: https://www.python.org/downloads/mac-osx/
[Python 3.5 for Linux]: https://www.python.org/downloads/source/
