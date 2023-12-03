import network
import ujson as json
import umachine as machine
from phew import server
from phew.template import render_template

from farset_tree import config
from farset_tree.util import GithubConfig, log, machine_reset, read_github_config


def route_index(request: server.Request):
  github_credentials = read_github_config() or GithubConfig(
    user='',
    repo='',
    ref='',
    token='',
    root='',
  )
  return render_template(
      '/farset_tree/server/index.html',
      user=github_credentials.user,
      repo=github_credentials.repo,
      ref=github_credentials.ref,
      root=github_credentials.root,
  )


def route_configure(request: server.Request):
  log('Saving github credentials...')
  log(json.dumps(request.form))

  with open(config.GITHUB_FILE, 'w') as f:
    json.dump(request.form, f)
    f.close()

  # Reboot from new thread after we have responded to the user.
  machine.Timer(mode=machine.Timer.ONE_SHOT, period=100, callback=lambda _: machine_reset())

  return server.redirect('/')


def route_log(request: server.Request):
  try:
    with open(config.LOG_FILE) as f:
      log = f.read()
      f.close()
  except:
    log = ''

  return render_template(
      '/farset_tree/server/log.html',
      log=log,
  )


def catch_all(request: server.Request):
  return server.redirect('/')


def start_server():
  network.hostname(config.HOSTNAME)

  phew_app = server.Phew()
  phew_app.add_route('/', route_index, methods=['GET'])
  phew_app.add_route('/configure', route_configure, methods=['POST'])
  phew_app.add_route('/log', route_log, methods=['GET'])
  phew_app.set_callback(catch_all)

  log('Starting server...')
  phew_app.run()
