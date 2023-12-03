import _thread
import gc

import ugit
import uos as os
import usys as sys

from farset_tree import config
from farset_tree.access_point import start_access_point
from farset_tree.server import start_server
from farset_tree.util import (
    connect_to_wifi,
    log,
    log_exception,
    read_github_config,
    read_wifi_config,
)


def thread(func):
  def wrapper(*args):
    _thread.start_new_thread(func, args)
  return wrapper


def log_and_ignore_exceptions(func):
  def wrapper(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except BaseException as e:
      log_exception(e)
  return wrapper


@log_and_ignore_exceptions
def git_pull():
  github_credentials = read_github_config()
  if not github_credentials:
    raise Exception('Invalid github credentials')

  github = ugit.Github(
      user=github_credentials.user,
      repo=github_credentials.repo,
      ref=github_credentials.ref,
      token=github_credentials.token,
  )
  github.pull(
      root=github_credentials.root,
      ignore=[
          '/lib/phew/',
          '/farset_tree/',
          '/main.py',
      ],
  )
  gc.collect()


@thread
@log_and_ignore_exceptions
def start_lights():
  if 'lights' in sys.modules:
    del sys.modules['lights']

  os.sync()
  import lights


def main():
  try:
    os.remove(config.LOG_FILE)
  except:
    pass

  wifi_credentials = read_wifi_config()
  if not wifi_credentials:
    log('Invalid wifi credentials')
    start_lights()
    start_access_point()
    return

  try:
    connected = connect_to_wifi(*wifi_credentials)
  except BaseException as e:
    log_exception(e)
    connected = False

  if not connected:
    start_lights()

    log('Bad wifi connection!')
    log(str(wifi_credentials))
    start_access_point()
    return

  git_pull()
  start_lights()

  start_server()


if __name__ == '__main__':
  main()
