# Space-X
A hyperparameter optimizer for [Moonline](https://gitlab.genzai.dev/boosting-alpha/moonline).

### Running
To run Space-X using `poetry`, use the following command:
```bash
$ poetry run python space-x -c <config_file>
```

### Generating Documentation
```bash
$ poetry run pdoc --config show_type_annotations=True --html --force space_x/
```

### Working on Documentation
`pdoc` can be switched into hot-reload mode by appending the following:
```bash
$ poetry run pdoc --config show_type_annotations=True --html --force space_x/ --http :
```

## Creating A Configuration File
In keeping with the way MoonLine handles options, they are specified via a configuration file in [INI](https://en.wikipedia.org/wiki/INI_file) format. This has the added benefit of being able to quickly switch between various configurations simply by pointing it at a different configuration file.

### Example Configuration
```ini
[MoonLine]
path = moonline-config.ini

[SpaceX]
iterations = 10

[Output]
path = out/
best_tearsheet = tearsheet_best.pdf

[Parameters]
path = params/
name = ParamsA
```

### Sections
#### MoonLine
Describes the MoonLine configuration to run.
##### `path`
The path to the MoonLine file configuration file().

#### Space-X
Space-X execution options.
##### `iterations`
The number of iterations to run. This giverns how many parameter combinations can be checked. More iterations means more space for testing combinations. This is multiplied by the number of jobs if parallel execution is enabled.
While the iterations will stay fixed (20 by default), if i.e. 4 worker processes are active, 4 times as many parameters will be explored within the same iteration.

#### Output
Paths for output artifacts.
##### `path`
The path to a directory. If the directory exists, it will be overwritten. This will output sub-directories with MD5 hashes for names containing the output of a specific MoonLine run.
##### `best_tearsheet`
The path to a file (`PDF`). If the file exists, it will be overwritten. This will output a tearsheet in PDF format containing multiple analytical charts to assess the performance of a given strategy. This tearsheet will only be generated for the run with the best parameters.

#### Parameters
Describes the parameter space to run.
##### `path`
The path to the directory containing the parameter file(s).
##### `name`
Either the exact filename of a parameter file inside the parameter directory (i.e. `crypto_parameters.py`) or the class name of a parameter definition.

If given a class name, Space-X will automatically look for and instantiate the given parameter class, so you can freely refactor your parameters and rename their files and it will still be able to pick it up.

If given a filename, only a single parameter class can be contained in the given file. When a class name is given, multiple parameters can be housed in the same file.

## Usage
```bash
Usage: space-x [OPTIONS] [ARGS]...

Options:
  -c, --config FILE  A file containing Space-X configuration options
                     [required]

  -v, --verbose
  --help             Show this message and exit.
```
