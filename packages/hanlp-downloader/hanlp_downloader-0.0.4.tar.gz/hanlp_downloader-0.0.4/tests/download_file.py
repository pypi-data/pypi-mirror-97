# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2021-03-04 19:04
import os
import platform
from hanlp_downloader import Downloader
from hanlp_downloader.log import DownloadCallback


def sha1sum(file_name):
    import hashlib
    BUF_SIZE = 65536

    sha1 = hashlib.sha1()

    with open(file_name, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()


def main():
    file_path = '1.zip'
    downloader = Downloader(
        'http://file.hankcs.com/hanlp/mtl/open_tok_pos_ner_srl_dep_sdp_con_electra_small_20201223_035557.zip', file_path, 2,
        high_speed=False,headers={
            'User-agent': f'HanLP/2.1.0.a1 ({platform.platform()})'})
    downloader.subscribe(DownloadCallback())
    downloader.start_sync()
    # assert sha1sum(file_path) == '79eaddb99a04763f1cce33cb2b1b81c0bbeeb77b'
    os.remove(file_path)


if __name__ == '__main__':
    main()
