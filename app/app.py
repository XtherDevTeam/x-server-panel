import flask,backend.vmrun,json,psutil,os,sys,socket,uuid,datetime,time

app = flask.app.Flask(__name__,
    static_url_path='/static/',
    static_folder='static',
    template_folder='template'
)

@app.route('/api', methods = ['GET'])
def indexOfAPI():
    r = flask.request.args.get('r')
    if r == 'vmlist':
        d = flask.request.args.get('d')
        if d == None: return {'status':'fail', 'reason': 'path or action is null'}
        if d == 'path': return json.dumps(backend.vmrun.get_registered_vms())
        if d == 'display_names': return json.dumps(backend.vmrun.get_registered_vm_names())
        if d == 'detail': return json.dumps(backend.vmrun.get_registered_vm_details())
    if r == 'vm':
        d = flask.request.args.get('d')
        p = flask.request.args.get('p')
        if d == None or p == None: return {'status':'fail', 'reason': 'path or action is null'}
        if p[0] == '"' or p[0] == '\'': p = p[1:-1]
        if d == 'name': return json.dumps(backend.vmrun.get_vm_name(p))
        if d == 'config': return json.dumps(backend.vmrun.vmx_read(p))
        if d == 'detail': return json.dumps(backend.vmrun.get_vm_detail(p))
        if d == 'start': return {'status': backend.vmrun.start_vm(p)}
        if d == 'stop': return {'status': backend.vmrun.stop_vm(p)}
        if d == 'reset': return {'status': backend.vmrun.reset_vm(p)}
        if d == 'suspend': return {'status': backend.vmrun.suspend_vm(p)}
    elif r == 'host_info':
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        mac = ":".join([mac[e:e+2] for e in range(0,11,2)])
        net = psutil.net_io_counters()
        o = psutil.disk_usage("/")
        
        return {
            'hostname': socket.gethostname(),
            'start_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
            'now_time': time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time())),
            'ip_addr': socket.gethostbyname(socket.gethostname()),
            'mac_addr': mac,
            'bytes_sent': '{0:.2f} Mb'.format(net.bytes_recv / 1024 / 1024),
            'bytes_recv': '{0:.2f} Mb'.format(net.bytes_sent / 1024 / 1024),
            'root_dir_total': str(int(o.total / (1024.0 * 1024.0 * 1024.0))) + "G",
            'root_dir_used': str(int(o.used / (1024.0 * 1024.0 * 1024.0))) + "G",
            'root_dir_free': str(int(o.free / (1024.0 * 1024.0 * 1024.0))) + "G",
            'cpu_count': psutil.cpu_count(logical=True) / psutil.cpu_count(logical=False),
            'all_cpu_core_count': psutil.cpu_count(),
            'cpu_usage': str(psutil.cpu_percent(1)) + '%',
            'memory_total': str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2)) + 'G',
            'memory_free': str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2)) + 'G',
        }
        

@app.route('/',methods = ['GET'])
def indexOfRoot():
    return flask.render_template('index.html')

@app.route('/vm',methods = ['GET'])
def indexOfVMList():
    return flask.render_template('index.html')

@app.route('/vm/view',methods = ['GET'])
def indexOfVMView():
    return flask.render_template('index.html')

app.run('0.0.0.0',5909)