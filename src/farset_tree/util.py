from collections import namedtuple

import phew
import ujson as json
import umachine as machine
import usys as sys
import utime as time

from farset_tree import config


def log(*lines: str):
  with open(config.LOG_FILE, 'a') as f:
    for line in lines:
      print(line)
      f.write(line)
      f.write('\n')


def log_exception(e: BaseException):
  with open(config.LOG_FILE, 'a') as f:
    sys.print_exception(e, f)


def machine_reset():
  time.sleep(1)
  log('Resetting...')
  machine.reset()


WifiConfig = namedtuple('WifiConfig', ('ssid', 'password'))


def read_wifi_config() -> WifiConfig | None:
  try:
    with open(config.WIFI_FILE, 'r') as f:
      data = json.load(f)
      return WifiConfig(
          ssid=data['ssid'],
          password=data.get('password'),
      )
  except:
    return None


def connect_to_wifi(ssid: str, password: str | None):
  log(f'Connecting to: {ssid}')
  wifi_current_attempt = config.WIFI_MAX_ATTEMPTS
  while wifi_current_attempt:
    ip_address = phew.connect_to_wifi(ssid, password)
    if phew.is_connected_to_wifi():
      log(f'Connected to wifi, IP address {ip_address}')
      return True

    wifi_current_attempt -= 1

  return False


GithubConfig = namedtuple('GithubConfig', ('user', 'repo', 'ref', 'token', 'root'))


def read_github_config() -> GithubConfig | None:
  try:
    with open(config.GITHUB_FILE, 'r') as f:
      data = json.load(f)
      return GithubConfig(
          user=data['user'],
          repo=data['repo'],
          ref=data['ref'],
          token=data.get('token'),
          root=data.get('root', ''),
      )
  except:
    return None
