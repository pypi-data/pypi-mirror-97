from pathlib import Path
from ifconf import configure_module, config_callback

@config_callback
def config(loader):
    loader.add_attr_path('ducts_home', Path('.'), help='root directory of all local path')
    loader.add_attr('pidpath', '{ducts_home}/.pid/{module}_{service}.pid', help='filepath to store PID')

conf = None

def get_conf():
    global conf
    if conf:
        return conf
    conf = configure_module(config)
    return conf
    
def get_pidfile(module, service):
    global conf
    conf = get_conf()
    path = Path(conf.pidpath.format(ducts_home=conf.ducts_home, module=module, service=service))
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    return str(path.resolve().absolute())

