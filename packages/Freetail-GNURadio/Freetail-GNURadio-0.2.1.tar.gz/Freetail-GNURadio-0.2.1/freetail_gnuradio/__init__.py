import os.path as osp
from pathlib import Path

with open(Path.resolve(Path(__file__)).parent / 'VERSION') as version_file:
    __version__ = version_file.read().strip()


def install_gr_blocks():
    """Installs Freetail blocks into GNU Radio Companion's path

    Note: This will overwrite any existing configuration of local_blocks_path
    """
    import configparser
    from gnuradio import gr

    # ensure config dir exists
    config_dir = Path(gr.userconf_path())
    config_dir.mkdir(exist_ok=True)
    
    config_filename = config_dir / "config.conf"

    config = configparser.ConfigParser()
    config.read(config_filename)

    if 'grc' not in config:
        config['grc'] = {}

    local_blocks_path = Path.resolve(Path(__file__)).parent / 'grc'

    config['grc']['local_blocks_path'] = str(local_blocks_path)
    with open(config_filename, 'w') as config_file:
        config.write(config_file)

