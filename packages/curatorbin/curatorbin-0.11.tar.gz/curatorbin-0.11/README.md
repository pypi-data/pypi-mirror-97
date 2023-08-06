Downloads [curator](https://github.com/mongodb/curator) as package data. 

The wheel file is a bit beefy, but curator can now be used as such:

```python
import curatorbin

curatorbin.run_curator(first_curator_arg, second_curator_arg)

```
Alternatively, you can get the path with `get_curator_path`.

## Building the package:

Batteries not included. You have to download the binaries into curatorbin yourself.
They are produced by an evergreen task and stored at
`https://s3.amazonaws.com/boxes.10gen.com/build/curator/curator-dist-%s-%s.tar.gz") % (os_platform, git_hash)`

First, make sure that the most current version of curator is in the appropriate dir:

```
curatorbin 
	macos/curator
	ubuntu1604/curator
	windows-64/curator.exe
```

Make sure the hash of the curator bin matches the hash in the `curatorbin/__init__.py` file.

To build for pip upload:

```
pip3 install -q build
python3 -m build
python3 -m twine upload --repository testpypi dist/*

```
See the following link for [credentials](https://packaging.python.org/tutorials/packaging-projects/).

Then, install with `pip3 install -vvv -i https://test.pypi.org/simple/ curatorbin==0.9` and test before uploading to pip.

You may wish to clean up old builds with `rm -rf curatorbin.egg-info dist build`
