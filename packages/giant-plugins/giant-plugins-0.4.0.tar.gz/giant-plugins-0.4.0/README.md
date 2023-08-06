# Giant Plugins

A re-usable package which can be used in any project that requires a base set of plugins. 

This will include a small set of plugins that are used in a large number of projects, but will not necessarily cover the full requirements. It will also provide a RichText field which can be used in other areas of the project
The RichText field uses ![summernote](https://github.com/summernote/summernote/) for styling the WYSIWYG widget.

## Installation

To install with the package manager, run:

    $ poetry add giant-plugins

You should then add `"giant_plugins"` to the `INSTALLED_APPS` in `base.py`.  

In order to run `django-admin` commands you will need to set the `DJANGO_SETTINGS_MODULE` by running

    $ export DJANGO_SETTINGS_MODULE=settings

## Configuration

This application exposes the following settings:

`SUMMERNOTE_CONFIG` which allows the user to configure a set of options for the redactor. For example the settings below will give you a basic setup,

```
SUMMERNOTE_CONFIG = (
    {
        "iframe": True,
        "summernote": {
            "airMode": False,
            # Change editor size
            "width": "100%",
            "height": "480",
            "lang": None,
            "toolbar": [
                ["style", ["style"]],
                ["font", ["bold", "underline", "clear"]],
                ["fontname", ["fontname"]],
                ["color", ["color"]],
                ["para", ["ul", "ol", "paragraph"]],
                ["table", ["table"]],
                ["insert", ["link", "picture", "video"]],
                ["view", ["fullscreen", "codeview", "help"]],
            ],
        },
    },
)

```

In order to specify a form to use for a specific plugin you should add something like this to your settings file:

```
<PLUGIN_NAME>_FORM = "<path.to.form.FormClass>"
```

Where PLUGIN_NAME is the capitalised name of the plugin (e.g `TEXTWITHIMAGEPLUGIN_FORM`) and the path to the form class as a string so it can be imported.

 ## Preparing for release
 
 In order to prep the package for a new release on TestPyPi and PyPi there is one key thing that you need to do. You need to update the version number in the `pyproject.toml`.
 This is so that the package can be published without running into version number conflicts. The version numbering must also follow the Semantic Version rules which can be found here https://semver.org/.
 
 
 ## Publishing
 
 Publishing a package with poetry is incredibly easy. Once you have checked that the version number has been updated (not the same as a previous version) then you only need to run two commands.
 
    $ `poetry build` 

will package the project up for you into a way that can be published.
 
    $ `poetry publish`

will publish the package to PyPi. You will need to enter the username and password for the account which can be found in the company password manager