aw-watcher-afk-barrier
==============

# [ActivityWatch](https://github.com/ActivityWatch/activitywatch) AFK Watcher for [Barrier](https://github.com/debauchee/barrier)

## What is it for?
A custom watcher for users using [ActivityWatch](https://github.com/ActivityWatch/activitywatch) together with [Barrier](https://github.com/debauchee/barrier)


Watches your keyboard and mouse activity to determine if you are AFK or not

**Replaces default `aw-watcher-afk`**
## How to install
To build your own packaged application, run `make package`

To install the latest git version directly from github without cloning, run
`pip install git+https://github.com/ActivityWatch/aw-watcher-afk-barrier.git`

To install from a cloned version, cd into the directory and run
`poetry install` to install inside an virtualenv. If you want to install it
system-wide it can be installed with `pip install .`, but that has the issue
that it might not get the exact version of the dependencies due to not reading
the poetry.lock file.


## Instructions
*Needs to run only on Barrier host.*

1. Disable default ActivityWatch `aw-watcher-afk`. For quick testing, you can just right-click on the tray icon and in modules deselect `aw-watcher-afk`, but if you want a permament solution, see [ErikBjare comment](https://github.com/ActivityWatch/activitywatch/issues/704#issuecomment-1009253158)
2. Run it via `poetry run aw-watcher-afk-barrier`

You can also make it autostart:
1. `make package`
2. `ln -s dist/aw-watcher-afk-barrier/aw-watcher-afk-barrier /usr/bin/`
3. Go to `~/.config/activitywatch/aw-qt/aw-qt.toml` and add `aw-watcher-afk-barrier` to `autostart_modules`



## Support
Linux support only for now. Feel free to do a PR for your platform.
