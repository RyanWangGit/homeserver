import argparse
from pathlib import Path
import logging
import requests
import json
from tqdm import tqdm
import re
import subprocess
import shutil

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def download(url, path: Path):
    if path.exists():
        raise ValueError(f'{path} already exists')
    response = requests.get(url, stream=True)
    total_length = int(response.headers['Content-length'])
    each_length = 1024 * 1024
    pbar = tqdm(total=total_length, unit='B', unit_divisor=1024, unit_scale=True)
    with path.open('wb') as fp:
        for chunk in response.iter_content(each_length):
            fp.write(chunk)
            pbar.update(each_length)
    pbar.close()


def updater_by_re(file: Path, version, check_url, check_re, download_url, name):
    response = requests.get(check_url)
    found = next(re.finditer(check_re, response.content.decode('utf-8')))
    filename = found.group(0)
    # split out the name and remove the suffix .jar
    latest = '-'.join(filename.split('-')[1:])[:-4]

    if version and version == latest:
        logger.info(f'Existing {version} is the latest, skipping')
        return

    download(
        f'{download_url}/{filename}', file.parent / f'{name}-{latest}.jar'
    )
    if version is not None:
        file.unlink()


def mcmmo(file: Path, version):
    response = requests.get('https://raw.githubusercontent.com/mcMMO-Dev/mcMMO/master/pom.xml')
    match = next(re.finditer(r'<version>(.*)</version>', response.content.decode('utf-8')))
    latest = match.group(1)
    if version and version == latest:
        logger.info(f'Existing {version} is the latest, skipping')
        return

    if version and version == latest:
        logger.info(f'Existing {version} is the latest, skipping')
        return

    script = f"""
    cd {file.parent.resolve()}
    rm -rf mcmmo-src
    git clone https://github.com/mcMMO-Dev/mcMMO.git mcmmo-src
    cd mcmmo-src
    mvn clean package install
    """
    with (file.parent / 'build_mcmmo.sh').open('w') as fp:
        fp.write(script)

    subprocess.run(['bash', (file.parent / 'build_mcmmo.sh').resolve()], shell=False)

    (file.parent / 'build_mcmmo.sh').unlink()

    shutil.move(
        (file.parent / 'mcmmo-src' / 'target' / 'mcMMO.jar').resolve(),
        (file.parent / f'mcmmo-{latest}.jar')
    )

    shutil.rmtree((file.parent / 'mcmmo-src').resolve())

    if version is not None:
        file.unlink()


def worldedit(file: Path, version):
    response = requests.get(
        r'https://builds.enginehub.org/job/worldedit/last-successful?branch=master',  allow_redirects=True
    )
    content = response.content.decode('utf-8')
    match = next(re.finditer(r'worldedit-bukkit-[0-9.]*-\w*-\w*\.jar', content))
    jar_name = match.group(0)
    match = next(re.finditer(r'\"build_id\":([0-9]*)', content))
    build_id = match.group(1)
    match = next(re.finditer(r'\"buildType\":\"([\w\d]*)\"', content))
    build_type = match.group(1)
    latest = '-'.join(jar_name.split('-')[1:])[:-4] + '-' + str(build_id)
    if version and version == latest:
        logger.info(f'Existing {version} is the latest, skipping')
        return
    download(
        f'https://ci.enginehub.org/repository/download/{build_type}/{build_id}:id/{jar_name}?branch=master&guest=1',
        file.parent / f'worldedit-{latest}.jar'
    )

    if version is not None:
        file.unlink()


def bluemap(file: Path, version):
    response = json.loads(requests.get('https://api.github.com/repos/BlueMap-Minecraft/BlueMap/releases').content)
    for asset in response[0]['assets']:
        if 'spigot' in asset['name']:
            latest = '-'.join(asset['name'].split('-')[1:])[:-4]
            if version and version == latest:
                logger.info(f'Existing {version} is the latest, skipping')
                return
            download(asset['browser_download_url'], file.parent / f'bluemap-{latest}.jar')
            break

    if version is not None:
        file.unlink()


def viaversion(file: Path, version):
    return updater_by_re(
        file,
        version,
        'https://ci.viaversion.com/job/ViaVersion/lastSuccessfulBuild/artifact/jar/target/',
        r'ViaVersion-[0-9.]*-\w*.jar',
        'https://ci.viaversion.com/job/ViaVersion/lastSuccessfulBuild/artifact/jar/target',
        'viaversion'
    )


def viabackwards(file: Path, version):
    return updater_by_re(
        file,
        version,
        'https://ci.viaversion.com/view/ViaBackwards/job/ViaBackwards/lastSuccessfulBuild/artifact/all/target/',
        r'ViaBackwards-[0-9.]*(-\w*)?.jar',
        'https://ci.viaversion.com/view/ViaBackwards/job/ViaBackwards/lastSuccessfulBuild/artifact/all/target',
        'viabackwards'
    )


def essentialsx(file: Path, version):
    return updater_by_re(
        file,
        version,
        'https://ci.ender.zone/job/EssentialsX/lastSuccessfulBuild/artifact/jars/',
        r'EssentialsX-[0-9.]*[\w\-+]*\.jar',
        'https://ci.ender.zone/job/EssentialsX/lastSuccessfulBuild/artifact/jars',
        'essentialsx'
    )


def mcmanager(file: Path, version):
    response = requests.get(
        'https://gist.githubusercontent.com/yxwangcs/b82abf7424d02b384e4e5ee5985552b1/raw/mcmanager.py'
    )
    file.write_bytes(response.content)


def papermc(file, version):
    # get latest papermc version
    body = json.loads(requests.get('https://papermc.io/api/v2/projects/paper').content)
    latest_version = '1.16.5' #body['versions'][-1]
    body = json.loads(requests.get(f'https://papermc.io/api/v2/projects/paper/versions/{latest_version}').content)
    latest_build = body['builds'][-1]
    body = json.loads(
        requests.get(
            f'https://papermc.io/api/v2/projects/paper/versions/{latest_version}/builds/{latest_build}'
        ).content
    )
    latest = '-'.join((str(latest_version), str(latest_build)))

    if version and version == latest:
        logger.info(f'Existing {version} is the latest, skipping')
        return

    filename = body['downloads']['application']['name']
    download_url = f'https://papermc.io/api//v2/projects/paper/versions/' \
                   f'{latest_version}/builds/{latest_build}/downloads/{filename}'
    # start download
    download(download_url, file.parent / f'paper-{latest_version}-{latest_build}.jar')

    if version is not None:
        file.unlink()


def update(mc_folder, plugin_folder, updaters):
    updater_dict = {updater.__name__: updater for updater in updaters}

    # first update papermc
    logger.info('Now updating papermc jar')
    papermc_jar = tuple(mc_folder.glob('paper*.jar'))
    if len(papermc_jar) <= 1:
        if len(papermc_jar) == 0:
            papermc_jar, version = mc_folder / 'paper.jar', None
        else:
            papermc_jar = papermc_jar[0]
            version = '-'.join(papermc_jar.stem.split('-')[1:])
        papermc(papermc_jar, version)
    else:
        logger.error(f'More than one paper jars are present in {mc_folder}, paper jar update skipped')

    logger.info('Now updating mcmanager')
    mcmanager(mc_folder / 'mcmanager.py', None)

    logger.info('Now updating plugins')
    # then update all plugins
    for updater in updaters:
        name = updater.__name__
        try:
            plugin_file = next(plugin_folder.glob(f'{name}*.jar'))
        except StopIteration:
            plugin_file = plugin_folder / f'{name}.jar'
        name, *rest = plugin_file.stem.split('-')
        name = name.lower()
        version = '-'.join(rest)
        if len(version) == 0:
            version = None
        logger.info(f'Updating {name} plugin')
        updater(plugin_file, version)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mc_folder', metavar='MC_FOLDER', type=str, nargs=1)
    parser.add_argument('plugin_folder', metavar='PLUGIN_FOLDER', type=str, nargs=1)
    results = parser.parse_args()
    mc_folder = Path(results.mc_folder[0])
    plugin_folder = Path(results.plugin_folder[0])
    for folder in (mc_folder, plugin_folder):
        if not (folder.exists() and folder.is_dir()):
            raise ValueError(f'{folder.resolve()} does not exist or is not a valid folder')
    update(mc_folder, plugin_folder, (essentialsx, viabackwards, viaversion, bluemap, worldedit, mcmmo))
