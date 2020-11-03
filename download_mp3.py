#!/usr/bin/env python3
# -*- coding: utf-8 -*-

google_drive_folder_name = "中国語学習"
temp_directory_name = "/tmp/chinese_lesson/"
target_directory_name = "/home/pi/chinese_lesson/"

import os
import glob
import hashlib
import shutil
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

def download_file_recursively(parent_id, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    print('{} created.'.format(dst_dir))

    file_list = drive.ListFile({'q': '"{}" in parents and trashed = false'.format(parent_id)}).GetList()

    for f in file_list:
        if f['mimeType'] == 'application/vnd.google-apps.folder':
            download_file_recursively(f['id'], os.path.join(dst_dir, f['title']))
        else:
            dst_path = os.path.join(dst_dir, f['title'])
            try:
                f.GetContentFile(dst_path)
                print('Downloaded {} to {}'.format(f['title'], dst_path))
            except:
                pass

def main():

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    download_file_recursively(
        drive.ListFile({'q': "title = '{}'".format(google_drive_folder_name)}).GetList()[0]['id'],
        temp_directory_name
    )

    for p in glob.glob(temp_directory_name + "/**" , recursive = True):
        relative_path = p[len(temp_directory_name):]
        target_path = target_directory_name + relative_path
        if os.path.isfile(p):
            if os.path.exists(target_path):
                with open(p, "rb") as f1:
                    with open(target_path, "rb") as f2:
                        checksum1 = hashlib.md5(f1.read()).hexdigest()
                        checksum2 = hashlib.md5(f2.read()).hexdigest()
                        if checksum1 != checksum2:
                            os.unlink(target_path)
                            shutil.copy2(p, target_path)
                            print(p + " copied to " + target_path)
                        else:
                            print("The same file already exists at " + target_path)
            else:
                shutil.copy2(p, target_path)
                print(p + " copied to " + target_path)
        elif os.path.isdir(p):
            try:
                os.mkdir(target_path)
                print(target_path + " created.")
            except FileExistsError:
                pass

    shutil.rmtree(temp_directory_name)

main()
