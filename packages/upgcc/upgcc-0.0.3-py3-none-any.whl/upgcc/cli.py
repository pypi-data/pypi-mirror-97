import os.path as osp
import os

import requests
from bs4 import BeautifulSoup
import argparse

from termcolor import colored


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', default='8.3.0', help='gcc version that you want to build.')
    parser.add_argument('--threads', default=os.cpu_count(), type=int,
                        help='use multiple threads to accelerate compiling.')
    parser.add_argument('--destdir', default=osp.expanduser('~/bin'), help='destination directory to store binaries.')
    args = parser.parse_args()

    root_site = 'https://mirrors.kernel.org/gnu/gcc'

    response = requests.get(root_site)
    if response.status_code != 200:
        raise RuntimeError()
    soup = BeautifulSoup(response.content, "html.parser", from_encoding="utf-8")

    found = False
    for a in soup.find_all('a'):
        print(a.contents[0])
        if a.contents[0] == f'gcc-{args.version}/':
            found = True
    if not found:
        raise RuntimeError(f'{args.version} not found.')

    url = f'https://mirrors.kernel.org/gnu/gcc/gcc-{args.version}/gcc-{args.version}.tar.gz'

    workdir = './tmp'
    os.makedirs(workdir, exist_ok=True)
    if not osp.exists(osp.join(workdir, f'gcc-{args.version}.tar.gz')):
        os.system(f'wget {url} -O {workdir}/gcc-{args.version}.tar.gz')
    os.system(f'cd {workdir} && tar xvzf gcc-{args.version}.tar.gz')
    prefix = osp.expanduser(f"{args.dest_dir}/gcc_{args.version.replace('-', '_')}")
    os.system(
        f'cd {workdir} &&  mkdir build-{args.version} && cd build-{args.version} && ../gcc-{args.version}/configure --build=x86_64-linux-gnu --prefix=/home/rakslice/gcc_{args.version.replace("-", "_")} --enable-checking=release --enable-languages=c,c++,fortran --disable-multilib --program-suffix=-{args.version} --prefix={prefix} && make -j {args.threads} && make install')
    print(colored('please run following command.', 'red'))
    print(f'export PATH={prefix}/bin:$PATH')


if __name__ == '__main__':
    main()
