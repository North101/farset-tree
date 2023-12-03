import phew
import ujson as json
import umachine as machine
from phew import dns, server
from phew.template import render_template

from farset_tree import config
from farset_tree.util import WifiConfig, log, machine_reset, read_wifi_config


def index(request):
  wifi_credentials = read_wifi_config() or WifiConfig(
    ssid='',
    password='',
  )
  return render_template(
      '/farset_tree/access_point/index.html',
      ssid=wifi_credentials.ssid,
  )


# microsoft windows redirects
def hotspot_ncsi(request: server.Request):
  print(request.uri)
  return '', 200


def hotspot_connecttest(request: server.Request):
  print(request.uri)
  return '', 200


def hotspot_redirect(request: server.Request):
  return server.redirect(config.AP_DOMAIN, 302)


# android redirects
def hotspot_generate_204(request: server.Request):
  return server.redirect(config.AP_DOMAIN, 302)


# apple redir
def hotspot_detect(request: server.Request):
  return '', 200


def configure(request: server.Request):
  log('Saving wifi credentials...')
  log(json.dumps(request.form))

  with open(config.WIFI_FILE, 'w') as f:
    json.dump(request.form, f)
    f.close()

  # Reboot from new thread after we have responded to the user.
  machine.Timer(mode=machine.Timer.ONE_SHOT, period=100, callback=lambda _: machine_reset())

  return server.redirect('/')


def catch_all(request: server.Request):
  return server.redirect(config.AP_DOMAIN)


def start_access_point():
  phew_app = server.Phew()
  phew_app.add_route('/', index, methods=['GET'])
  phew_app.add_route('/configure', configure, methods=['POST'])
  phew_app.add_route('/ncsi.txt', hotspot_ncsi, methods=['GET'])
  phew_app.add_route('/connecttest.txt', hotspot_connecttest, methods=['GET'])
  phew_app.add_route('/redirect', hotspot_redirect, methods=['GET'])
  phew_app.add_route('/generate_204', hotspot_generate_204, methods=['GET'])
  phew_app.add_route('/hotspot-detect.html', hotspot_detect, methods=['GET'])
  phew_app.set_callback(catch_all)

  log('Starting access point...')
  ap = phew.access_point(config.HOSTNAME, config.AP_PASSWORD)
  ip = ap.ifconfig()[0]
  dns.run_catchall(ip)
  phew_app.run()
