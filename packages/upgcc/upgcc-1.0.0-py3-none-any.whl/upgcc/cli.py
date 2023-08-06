import os.path as osp
import os
from packaging import version
import requests
from bs4 import BeautifulSoup
import argparse

from termcolor import colored


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', required=True, help='gcc version that you want to build.')
    parser.add_argument('--threads', default=os.cpu_count(), type=int,
                        help='use multiple threads to accelerate compiling. Default using all threads.')
    parser.add_argument('--dest_dir', default=osp.expanduser('~/bin'),
                        help='destination directory to store binaries. Default store to ~/bin')
    args = parser.parse_args()

    root_site = 'https://mirrors.kernel.org/gnu/gcc'

    response = requests.get(root_site)
    if response.status_code != 200:
        raise RuntimeError()
    soup = BeautifulSoup(response.content, "html.parser", from_encoding="utf-8")

    valid_versions = []
    for a in soup.find_all('a'):
        ver: str = a.contents[0][4:-1]
        if isinstance(version.parse(ver), version.Version):
            valid_versions.append(ver)
    if args.version not in valid_versions:
        print(f'{args.version} not found.')
        print('Valid versions', valid_versions)
        exit(1)

    url = f'https://mirrors.kernel.org/gnu/gcc/gcc-{args.version}/gcc-{args.version}.tar.gz'

    workdir = './tmp'
    os.makedirs(workdir, exist_ok=True)
    if not osp.exists(osp.join(workdir, f'gcc-{args.version}.tar.gz')):
        ret = os.system(f'wget {url} -O {workdir}/gcc-{args.version}.tar.gz')
        if ret != 0: exit(1)
    ret = os.system(f'cd {workdir} && tar xvzf gcc-{args.version}.tar.gz')
    if ret != 0: exit(1)
    prefix = osp.expanduser(f"{args.dest_dir}/gcc_{args.version.replace('-', '_')}")
    if osp.exists(workdir):
        os.system(f'/bin/rm -rf {workdir}/build-{args.version}')
    command = f'cd {workdir} && mkdir -p build-{args.version} && cd build-{args.version} && ../gcc-{args.version}/configure --build=x86_64-linux-gnu --enable-checking=release --enable-languages=c,c++,fortran --disable-multilib --program-suffix=-{args.version} --prefix={prefix} '
    print(command)
    ret = os.system(command)
    if ret != 0: exit(1)
    command = f'cd {workdir}/build-{args.version} && make -j {args.threads}'
    print(command)
    os.system(command)
    if ret != 0: exit(1)
    os.system(f'cd {workdir}/build-{args.version} && make install')
    if ret != 0: exit(1)
    print(colored('Build success. please run following command.', 'red'))
    print(f'export PATH={prefix}/bin:$PATH')


if __name__ == '__main__':
    main()
