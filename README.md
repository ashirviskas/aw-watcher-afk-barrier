aw-watcher-afk-barrier
==============

# ActivityWatcher Barrier

## What is it for?
A custom watcher for users using ActivityWatcher together with [Barrier](https://github.com/debauchee/barrier)

Watches your keyboard and mouse activity to determine if you are AFK or not

## How to install
To build your own packaged application, run `make package`

To install the latest git version directly from github without cloning, run
`pip install git+https://github.com/ActivityWatch/aw-watcher-afk-barrier.git`

To install from a cloned version, cd into the directory and run
`poetry install` to install inside an virtualenv. If you want to install it
system-wide it can be installed with `pip install .`, but that has the issue
that it might not get the exact version of the dependencies due to not reading
the poetry.lock file.


## Support
Linux support only for now. Feel free to do a PR for your platform.
