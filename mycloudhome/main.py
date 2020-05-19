import click
import mycloudhome.configure as configure
import mycloudhome.auth as auth
import mycloudhome.device as device
import mycloudhome.filemanagement as filemanagement
import mycloudhome.resumablefiles as resumablefiles
import mycloudhome.utils as utils


@click.group()
@click.option('--device', help='WD mycloudhome device id, can leave empty')
@click.option('--debug', is_flag=True, default=False, help='Show debug log')
def cli(device, debug):
    configure.debug = debug
    configure.device = device
    pass


@cli.command()
@click.option('--username', prompt=True, help='wd mycloudhome username')
@click.option('--password', prompt=True, hide_input=True)
def login(username, password):
    """GET WD MY CLOUD HOME ACCESS TOKEN."""
    click.echo('login...')
    configure.fetch_endpoint()
    click.echo(utils.pretty(auth.login(username, password)))


@cli.command()
def devices():
    """Get the Devices that User is attached to."""
    click.echo(utils.pretty(device.get_list_by_user_id(configure.get(
        configure.get_default_profile(), 'user_id'))))


def if_wd_path(ctx, param, value):
    # print(ctx, param, value)
    if utils.is_wd_path(value):
        return value
    raise click.BadParameter('{} is not a wd path'.format(value))


def if_local_dir(ctx, param, value):
    # print(ctx, param, value)
    if utils.is_local_dir(value):
        return value
    raise click.BadParameter('{} is not exist or not a dir'.format(value))

def if_local_file(ctx, param, value):
    # print(ctx, param, value)
    if utils.is_local_file(value):
        return value
    raise click.BadParameter('{} is not exist or is a dir'.format(value))

@cli.command()
@click.option('--wduri', prompt=True, callback=if_wd_path, help='Search files by parent directory. wd:// is the root')
@click.option('--pagetoken', default="", help='The pageToken obtained from the last response.')
def ls(wduri, pagetoken):
    """List WD objects under a prefix or under the root."""
    """<WDUri>"""
    click.echo(utils.pretty(
        filemanagement.get_file_list(wduri, pagetoken)))


@cli.command()
@click.option('--src', prompt=True, callback=if_wd_path, help='source file path in wd uri format')
@click.option('--dst', prompt=True, callback=if_wd_path, help='target file path in wd uri format')
def mv(src, dst):
    """Moves a WD object to another location in WD MY CLOUD HOME."""
    """<WDUri> <WDUri>"""
    filemanagement.move(src, dst)


@cli.command()
@click.option('--wduri', prompt=True, callback=if_wd_path, help='target file path in wd uri format')
@click.option('--name', prompt=True, help='new name')
def rename(wduri, name):
    """Rename a WD object."""
    """<WDUri> name"""
    filemanagement.rename(wduri, name)


@cli.command()
@click.option('--wduri', prompt=True, callback=if_wd_path, help='target file path in wd uri format')
def rm(wduri):
    """Deletes an WD object."""
    """<WDUri>"""
    filemanagement.delete(wduri)


@cli.command()
@click.option('--wduri', prompt=True, callback=if_wd_path, help='target file path in wd uri format')
@click.option('--localpath', prompt=True, callback=if_local_dir, help='target file path in wd uri format')
def download(wduri, localpath):
    """Copies a WD object to location locally."""
    """<WDUri> <LocalPath>"""
    filemanagement.download(wduri, localpath)


@cli.command()
@click.option('--wduri', prompt=True, callback=if_wd_path, help='target file path in wd uri format')
def mkdir(wduri):
    """Create an WD dir."""
    """<WDUri>"""
    filemanagement.mkdir(wduri)


@cli.command()
@click.option('--localpath', prompt=True, callback=if_local_file, help='target file path in wd uri format')
@click.option('--wduri', prompt=True, callback=if_wd_path, help='target file path in wd uri format')
def upload(localpath,wduri):
    """Copies a local file to location in WD MY CLOUD HOME."""
    """<LocalPath> <WDUri>"""
    resumablefiles.upload(localpath,wduri)


# TODO
# @cli.command()
# def sync():
#     pass

if __name__ == '__main__':
    cli()
