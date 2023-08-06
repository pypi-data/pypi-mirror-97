#!/usr/bin/env python3
'''
Copyright 2018-2021 Autograders

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import os
import sys
import json
import zipfile
import argparse
import requests
from getpass import getpass
from tabulate import tabulate


# CLI title
__TITLE__ = '''

   ___       __                        __
  / _ |__ __/ /____  ___ ________ ____/ /__ _______
 / __ / // / __/ _ \\/ _ `/ __/ _ `/ _  / -_) __(_-<
/_/ |_\\_,_/\\__/\\___/\\_, /_/  \\_,_/\\_,_/\\__/_/ /___/
                   /___/

            Command Line Interface
               Autograders.org
'''

# Test flag
TEST = False
# API URL
API_URL = 'http://localhost:8080' if TEST else 'https://api.autograders.org'
# Sign Up URL
SIGN_UP_URL = f'{API_URL}/user'
# Verify URL
VERIFY_URL = f'{API_URL}/user/verify'
# Sign In URL
SIGN_IN_URL = f'{API_URL}/auth/signin'
# Upload task URL
UPLOAD_TASK_URL = f'{API_URL}/submit'
# Get Task URL
GET_TASK_URL = f'{API_URL}/task/%s'
# Pin URL
PIN_URL = f'{API_URL}/pin'
# Task stats URL
TASK_STATS_URL = f'{API_URL}/submit/%s?type=last'
# Autograder directory
AUTOGRADER_DIR = '.autograder'
# Autograder config file
AUTOGRADER_CFG = 'autograder.json'


def write_file(name, text):
    if not os.path.exists(AUTOGRADER_DIR):
        os.mkdir(AUTOGRADER_DIR)
    with open(os.path.join(AUTOGRADER_DIR, name), 'w') as f:
        f.write(text)
        f.close()


def read_file(name):
    with open(os.path.join(AUTOGRADER_DIR, name), 'r') as f:
        return f.read().strip()


def file_exists(name):
    return os.path.exists(os.path.join(AUTOGRADER_DIR, name))


def read_config():
    if not os.path.exists(AUTOGRADER_CFG):
        print(f'Autograder configuration file "{AUTOGRADER_CFG}" not found')
        sys.exit(1)
    try:
        with open(AUTOGRADER_CFG, 'r') as f:
            return json.loads(f.read().strip())
    except Exception:
        print(f'Could not parse autograder configuration file "{AUTOGRADER_CFG}"')
        sys.exit(1)


def register():
    try:
        print(__TITLE__)
        print('User Registration')
        print('')
        # set payload
        payload = {
            'fullName': input(' - Full Name: ').strip(),
            'email': input(' - Email: ').strip(),
            'password': getpass(' - Password: ').strip()
        }
        print('')
        r = requests.post(SIGN_UP_URL, json=payload)
        data = r.json()
        if r.status_code != 201:
            print(' [*] Error: ' + data['message'])
            sys.exit(1)
        else:
            print(' [*] Success: ' + data['message'])
            sys.exit(0)
    except Exception:
        print(' [*] Fatal: Could not register user')
        sys.exit(1)


def pin():
    try:
        print(__TITLE__)
        print('Generate New Pin Code')
        print('')
        # set payload
        payload = {
            'email': input(' - Email: ').strip(),
        }
        print('')
        r = requests.post(PIN_URL, json=payload)
        data = r.json()
        if r.status_code != 201:
            print(' [*] Error: ' + data['message'])
            sys.exit(1)
        else:
            print(' [*] Success: ' + data['message'])
            sys.exit(0)
    except Exception:
        print(' [*] Fatal: Could not generate a new pin code')
        sys.exit(1)


def verify():
    try:
        print(__TITLE__)
        print('User Verification')
        print('')
        # set payload
        payload = {
            'email': input(' - Email: ').strip(),
            'code': getpass(' - Pin Code: ').strip()
        }
        print('')
        r = requests.post(VERIFY_URL, json=payload)
        data = r.json()
        if r.status_code != 201:
            print(' [*] Error: ' + data['message'])
            sys.exit(1)
        else:
            print(' [*] Success: ' + data['message'])
            sys.exit(0)
    except Exception:
        print(' [*] Fatal: Could not register user')
        sys.exit(1)


def login(force=False):
    try:
        if force:
            print('Enter credentials:')
            print('')
        # get cached token
        if not force and file_exists('auth'):
            return read_file('auth').split('|')
        # set payload
        payload = {
            'email': input(' - Email: ').strip(),
            'password': getpass(' - Password: ').strip()
        }
        print('')
        r = requests.post(SIGN_IN_URL, json=payload)
        data = r.json()
        if r.status_code != 201:
            print(' [*] Error: ' + data['message'])
            sys.exit(1)
        else:
            user_id = data['user_attributes']['id']
            token = data['access_token']
            write_file('auth', f'{user_id}|{token}')
            return user_id, token
    except Exception:
        print(' [*] Fatal: Could not login')
        sys.exit(1)


def stats(force=False):
    try:
        print(__TITLE__)
        print('Get Task Stats')
        print('')
        config = read_config()
        task_id = config.get('id')
        user_id, token = login(force=force)
        headers = { 'Authorization': token }
        r = requests.get(TASK_STATS_URL % task_id, headers=headers)
        grade = r.json()
        if r.status_code == 200:
            print(' - Queued: %s' % grade['queued'])
            print(' - Grade: %.2f/100' % grade['grade'] )
            print(' - Created At: ' + grade['createdAt'])
            print(' - Updated At: ' + grade['updatedAt'])
            details = grade['details']
            t = []
            for d in details:
                t.append([d['name'], d['grade'], d['message']])
            if len(t) > 0:
                print('')
                print('Details:')
                print('')
                print(tabulate(t, headers=['Name', 'Grade', 'Message'], tablefmt="fancy_grid"))
            stdout = grade['stdout'].strip()
            if stdout != '':
                print('')
                print('stdout:')
                print(grade['stdout'])
            stderr = grade['stderr'].strip()
            if stderr != '':
                print('')
                print('stderr:')
            print('')
            print(' [*] Success')
            sys.exit(1)
        elif not force and (r.status_code == 401 or r.status_code == 403):
            stats(force=True)
        else:
            print(' [*] Error: ' + grade['message'])
            sys.exit(1)
    except Exception as e:
        print(' [*] Fatal: Could not get task stats')
        sys.exit(1)


def get_task_files(config, force=False):
    try:
        task_id = config.get('id')
        user_id, token = login(force=force)
        headers = { 'Authorization': token }
        r = requests.get(GET_TASK_URL % task_id, headers=headers)
        data = r.json()
        if r.status_code == 200:
            return data['files']
        elif not force and (r.status_code == 401 or r.status_code == 403):
            return get_task_files(config, force=True)
        else:
            print(' [*] Error: ' + data['message'])
            sys.exit(1)
    except Exception:
        print(' [*] Fatal: Could not get task files')
        sys.exit(1)


def zip_files(files, task_id, user_id):
    try:
        filename = os.path.join(AUTOGRADER_DIR, f'{task_id}-{user_id}.zip')
        # create zip file
        with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zip:
            # get all files to zip
            for f in files:
                zip.write(f)
            zip.close()
        return open(filename, 'rb'), filename
    except Exception:
        print(' [*] Fatal: Could not generate zip file')
        sys.exit(1)


def upload(force=False):
    try:
        print(__TITLE__)
        print('Upload Task')
        print('')
        config = read_config()
        task_id = config.get('id')
        files = get_task_files(config)
        user_id, token = login(force=force)
        headers = { 'Authorization': token }
        f, filename = zip_files(files, task_id, user_id)
        files = { 'file': f }
        r = requests.post(UPLOAD_TASK_URL, files=files, headers=headers)
        data = r.json()
        if r.status_code == 201:
            print(' [*] Success: ' + data['message'])
        elif not force and (r.status_code == 401 or r.status_code == 403):
            upload(force=True)
        else:
            print(' [*] Error: ' + data['message'])
            sys.exit(1)
    except Exception:
        print(' [*] Fatal: Could not upload task')
        sys.exit(1)


def autograder(args):
    '''Autograder CLI'''
    try:
        if args.upload:
            upload()
        elif args.stats:
            stats()
        elif args.register:
            register()
        elif args.verify:
            verify()
        elif args.pin:
            pin()
    except KeyboardInterrupt:
        print()
        print()


def main():
    parser = argparse.ArgumentParser(description='Autograders Command Line Interface')
    parser.add_argument('--upload', action='store_true', help='Upload files to autograder')
    parser.add_argument('--stats', action='store_true', help='Get task stats')
    parser.add_argument('--register', action='store_true', help='Register user')
    parser.add_argument('--verify', action='store_true', help='Verify user')
    parser.add_argument('--pin', action='store_true', help='Send a new pin code')
    args = parser.parse_args()
    autograder(args)


if __name__ == '__main__':
    main()
