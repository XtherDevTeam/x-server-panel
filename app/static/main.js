let mainForm = new x_object("xf-body");
function load_sidebar() {
    let vmlist = fetch_json_api('/api?r=vmlist','get');
    mainForm.insert('<div id="sidebar"></div>');
    let temp = new x_object("sidebar");
    temp.setCSS({
        "float":"left"
    })
}

function load_server_summary() {
    let host_info = fetch_json_api('/api?r=host_info','get');
    
}

function load_all() {
    
}