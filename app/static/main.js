let mainForm = new x_object("xf-body");

function load_sidebar() {
    let namelist = fetch_json_api('/api?r=vmlist&d=display_names','get');
    let vmxlist = fetch_json_api('/api?r=vmlist&d=path','get');
    for (let i = 0; i < namelist.length; i++) {
        const element = namelist[i], element1 = vmxlist[i];
        m('slide-out').insert('<li><a class="waves-effect" href="/vm/view?vmx=\'' + element1 + '\'">' + element + '</a></li>');
    }
}

function load_server_summary() {
    let host_info = fetch_json_api('/api?r=host_info','get');
    m('main-panel').setHtml('');
    m('main-panel').insert('<h2><i class="fas fa-server"></i>&nbsp;&nbsp;' + host_info['hostname'] + '</h2>');
    m('main-panel').insert('Now time: <span id="now_time">' + host_info['now_time'] + '</span><br>');
    m('main-panel').insert('Start time: <span id="start_time">' + host_info['start_time'] + '</span><br>');
    m('main-panel').insert('<br>');
    m('main-panel').insert('IP Address: <span id="ip_addr">' + host_info['ip_addr'] + '</span><br>');
    m('main-panel').insert('MAC Address: <span id="mac_addr">' + host_info['mac_addr'] + '</span><br>');
    m('main-panel').insert('<br>');
    m('main-panel').insert('CPU Usage: <span id="cpu_usage">' + host_info['cpu_usage'] + '</span><br>');
    m('main-panel').insert('<br>');
    m('main-panel').insert('Recved bytes: <span id="bytes_recv">' + host_info['bytes_recv'] + '</span><br>');
    m('main-panel').insert('Sent bytes: <span id="bytes_sent">' + host_info['bytes_sent'] + '</span><br>');
    m('main-panel').insert('<br>');
    m('main-panel').insert('Memory Free: <span id="memory_free">' + host_info['memory_free'] + '</span>' + ' of <span id="memory_total">' + host_info['memory_total'] + '</span><br>');
    m('main-panel').insert('Storage Used: <span id="root_dir_used">' + host_info['root_dir_used'] + '</span>' + ' of <span id="root_dir_total">' + host_info['root_dir_total'] + '</span><br>');
}

function load_vm_list(){
    let table_str = '';
    table_str = '<table style="">\
    <thead>\
    <tr><th style="width: 5rem;">Name</th><th style="width: 50%;">Path</th><th>Status</th><th>Action</th></tr>\
    </thead>';
    table_str += '<tbody>\n';
    let vm_details = fetch_json_api('/api?r=vmlist&d=detail','get')
    for (let index = 0; index < vm_details.length; index++) {
        const e = vm_details[index];
        console.log(e)
        table_str += '<tr>\n';
        table_str += '<td class="overflow"><a href="/vm/view?vmx=\'' + e['vmxPath'] + '\'">' + e['name'] + '</a></td>\n';
        table_str += '<td class="overflow">' + e['vmxPath'] + '</td>\n';
        if(e['running'] == 1){
            table_str += '<td><span style="color: green;"><i class="fas fa-check-circle"></i> Online</span></td>\n';
        }else{
            table_str += '<td><span style="color: red;"><i class="fas fa-exclamation-triangle"></i> Offline</span></td>\n';
        }
        table_str += '<td><button type="button" onclick="vm_operation(\'' + e['vmxPath'] + '\',\'unregister\')" class="btn btn-primary">Unregister</button>&nbsp;&nbsp;<button type="button" onclick="vm_operation(\'' + e['vmxPath'] + '\',\'remove\')" class="btn btn-primary">Remove</button></td>'

        table_str += '</tr>\n';
    }
    table_str += '</tbody>\n';
    table_str += '</table>\n';
    console.log(table_str)
    m('main-panel').insert(table_str);
}

function main_page_load_all() {
    load_server_summary();
    setInterval(function () {
        load_server_summary();
    },5000);
}

function vm_list_page_load_all() {
    m('main-panel').insert('<br>');
    m('main-panel').insert('<a id="btn-vm-new" href="/vm/new">New virtual machine</a> ');
    m('main-panel').insert('<a id="btn-vm-register" href="/vm/register">Register a virtual machine</a><br>');
    m('main-panel').insert('<br>');
    m('btn-vm-new').setClassList(['btn', 'btn-primary', 'ripple-surface']);
    m('btn-vm-register').setClassList(['btn', 'btn-primary', 'ripple-surface']);
    load_vm_list();
    m('main-panel').insert('<br>');
}

function vm_view_page_load_all() {
    m('main-panel').setClassList(["x-container"]);
    console.log(arg('vmx'));
    let vmx_detail = fetch_json_api('/api?r=vm&d=detail&p=' + arg('vmx'),'get')
    let table_str = '';
    table_str = '<table style="width: 500px;table-layout: fixed; overflow: hidden;float: left;">\
    <thead>\
    <tr><th>Item</th><th style="width: 70%;">Value</th></tr>\
    </thead>';
    table_str += '<tbody>\n';
    for (const key in vmx_detail) {
        if (Object.hasOwnProperty.call(vmx_detail, key)) {
            const element = vmx_detail[key];
            table_str += '<tr>';
            table_str += '<td><div>' + key + '</div></td>';
            table_str += '<td><div class="overflow" style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">' + element + '</div></td>';
            table_str += '</tr>';
        }
    }
    table_str += '</tbody>\n</table>';
    m('main-panel').insert('<h2>' + vmx_detail['name'] + '</h2>');
    m('main-panel').insert(table_str);

    m('main-panel').insert('<div id="xf-rightside" style="width: auto;float: left;"></div>');
    if(vmx_detail['remoteDisplay'] == true && vmx_detail['running'] == 1){
        m('xf-rightside').insert('<a href="vnc://' + window.location.hostname + ':' + vmx_detail['remoteDisplayPort'] + '" class="btn btn-primary">Open VNC Connection</a>');
    }else{
        m('xf-rightside').insert('<a href="vnc://" class="btn btn-primary" disabled alt="VM disabled remoteDisplay">Open VNC Connection(Host down or VNC connection is not configured)</a>');
    }
    m('xf-rightside').insert('<br><br>');
    m('xf-rightside').insert('<a href="javascript:;" class="btn btn-primary" onclick="vm_operation(' + arg('vmx') + ',\'start\')" >Start</a>&nbsp;');
    m('xf-rightside').insert('<a href="javascript:;" class="btn btn-primary" onclick="vm_operation(' + arg('vmx') + ',\'stop\')" >Stop</a>&nbsp;');
    m('xf-rightside').insert('<a href="javascript:;" class="btn btn-primary" onclick="vm_operation(' + arg('vmx') + ',\'reset\')" >Reset</a>&nbsp;');
    m('xf-rightside').insert('<a href="javascript:;" class="btn btn-primary" onclick="vm_operation(' + arg('vmx') + ',\'suspend\')" >Suspend</a>&nbsp;');
    m('xf-rightside').insert('<br><br>');

    m('xf-rightside').insert('<div id="xf-cdrom-loader"></div>');
    m('xf-cdrom-loader').makeDirectorySelector('CD-ROM Loaded media:','cdrom-media');
    // console.log(m('xf-cdrom-loader').dom);
    m('xf-rightside').insert('<br>');
    m('xf-rightside').insert('<a href="javascript:;" class="btn btn-primary" onclick="load_cdrom_media(' + arg('vmx') + ')" >Load</a>&nbsp;');

    document.getElementsByName('cdrom-media')[0].setAttribute("value",vmx_detail['cdrom-media'])

    m('main-panel').insert('<div style="clear:both;"></div>');
}

function load_cdrom_media(vmx_path) {
    if(vmx_path[0] != '\'' || vmx_path[0] != '"') vmx_path = '\'' + vmx_path + '\'';
    let media = d(document.getElementsByName('cdrom-media')[0]).getValue();
    media = "'" + media + "'";
    fetch_json_api_nosync('/api?r=vm&d=cdrom-change&media=' + media + '&p=' + vmx_path,'get',function (result) {
        if(result['status'] == true){
            window.location.reload();
        }else{
            alert('Change CD-ROM Media Failed.');
        }
    })
}

function submit_create_vm_request(){
    let vm_name = m('vm_name').getValue();
    let guest_os = m('guest_os').getValue();
    let memory = m('memory').getValue();
    let disk = m('disk').getValue();
    let remote_port = m('remote_port').getValue();
    let cpu_cores = m('cpu_cores').getValue();
    let finalUrl = '/api?r=vm&d=new&name=' + vm_name +
        '&guestOS=' + guest_os + 
        '&memory=' + memory + 
        '&disk=' + disk +
        '&remotePort=' + remote_port + 
        '&cores=' + cpu_cores;
    fetch_json_api_nosync(finalUrl,'get',function (result) {
        if(result['status'] == true){
            window.location = '/vm';
        }else{
            alert('Create VM Failed!');
        }
    })
}

function vm_new_page_load_all() {
    m('main-panel').insert('<div id="uploader"></div>');
    m('uploader').nextLine();
    m('uploader').createInput('vm_name','vm_name','text','The name of virtual machine');
    m('vm_name').setCSS({
        'width': '80%'
    });
    m('uploader').nextLine();

    m('uploader').createInput('guest_os','guest_os','text','Virtual machine guest OS type','window9-64');
    m('guest_os').setCSS({
        'width': '80%'
    });
    m('uploader').nextLine();

    m('uploader').createInput('memory','memory','number','Virtual machine memory size',2048);
    m('memory').setCSS({
        'width': '80%'
    });
    m('uploader').nextLine();

    m('uploader').createInput('disk','disk','text','Virtual machine main disk size','32G');
    m('disk').setCSS({
        'width': '80%'
    });
    m('uploader').nextLine();

    m('uploader').createInput('remote_port','remote_port','number','Virtual machine remote port',5901);
    m('remote_port').setCSS({
        'width': '80%'
    });
    m('uploader').nextLine();

    m('uploader').createInput('cpu_cores','cpu_cores','number','Virtual machine CPU Cores',2);
    m('cpu_cores').setCSS({
        'width': '80%'
    });
    m('uploader').nextLine();

    m('uploader').createButton('submit','Submit',"submit_create_vm_request();");
    m('uploader').nextLine();
    m('uploader').nextLine();
}

function vm_register_page_load_all(){
    m('main-panel').insert('<div id="path-select"></div>');
    m('path-select').makeDirectorySelector('Select a vmx file:', 'path-selector');
    m('uploader').nextLine();
    
    m('main-panel').createButton('submit','Submit',"vm_operation(document.getElementsByName('path-selector')[0].value,'register');");
    m('uploader').nextLine();
    m('uploader').nextLine();
}

function universal_load_all(){
    mainForm.insert('<div id="main-panel"></div><br><br>');
    m('main-panel').setClassList(["x-container"]);
    m('main-panel').setCSS({
        'width': '90%',
        'margin': '0 auto',
        'padding-left': '20px',
        'top': '50px',
        'padding-top': '5px',
        'position': 'relative',
    });
    load_sidebar();
}