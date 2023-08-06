Utility functions and classes for configuration files.

*Latest release 20210306*:
Fix imports from collections.abc.

## Class `ConfigSectionWatcher(collections.abc.Mapping,collections.abc.Collection,collections.abc.Sized,collections.abc.Iterable,collections.abc.Container)`

A class for monitoring a particular clause in a config file.

### Method `ConfigSectionWatcher.__init__(self, config, section, defaults=None)`

Initialise a ConfigSectionWatcher to monitor a particular section
of a config file.
`config`: path of config file, or ConfigWatcher
`section`: the section to watch
`defaults`: the defaults section to use, default 'DEFAULT'

### Method `ConfigSectionWatcher.__getitem__(self, key)`

#### Mapping methods.

### Method `ConfigSectionWatcher.as_dict(self)`

Return the config section as a dict.

### Method `ConfigSectionWatcher.keys(self)`

Return the keys of the config section.

### Property `ConfigSectionWatcher.path`

The pathname of the config file.

## Class `ConfigWatcher(collections.abc.Mapping,collections.abc.Collection,collections.abc.Sized,collections.abc.Iterable,collections.abc.Container)`

A monitor for a windows style .ini file.
The current SafeConfigParser object is presented as the .config property.

### Method `ConfigWatcher.__getitem__(self, *a, **kw)`

Return the ConfigWatcher for the specified section.

### Method `ConfigWatcher.as_dict(self)`

Construct and return a dictionary containing an entry for each section
whose value is a dictionary of section items and values.

### Property `ConfigWatcher.config`

Inner wrapper for `func`.

### Property `ConfigWatcher.path`

The path to the config file.

### Method `ConfigWatcher.section_keys(self, section)`

Return the field names for the specified section.

### Method `ConfigWatcher.section_value(self, section, key)`

Return the value of [section]key.

## Function `load_config(config_path, parser=None)`

Load a configuration from the named `config_path`.

If `parser` is missing or None, use SafeConfigParser (just
ConfigParser in Python 3).
Return the parser.

# Release Log



*Release 20210306*:
Fix imports from collections.abc.

*Release 20190101*:
Internal changes.

*Release 20160828*:
Update metadata with "install_requires" instead of "requires".

*Release 20150118*:
Initial PyPI release.
