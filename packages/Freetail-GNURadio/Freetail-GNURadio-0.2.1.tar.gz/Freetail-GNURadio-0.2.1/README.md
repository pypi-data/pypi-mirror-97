**freetail-gnuradio: GNU Radio blocks for use with the Freetail module.**

Includes GNU Radio Companion definitions, which will appear under a new category labelled
Radar and Sonar.

For GNU Radio Companion to find these blocks, they will need to be included within the
configuration file `~/.gnuradio/config.conf`. Under the section `[grc]`, the setting
`module_blocks_path` needs to be set appropriately. This can be done automatically
by running the following at the command line:

`python -c "import freetail_gnuradio; freetail_gnuradio.install_gr_blocks()"`

Note that this will overwrite any previous custom block settings, so if you
have other custom blocks, you should update this setting manually.

When opening GNU Radio Companion, you should see the blocks appear under a new
section `Radar and Sonar`.

