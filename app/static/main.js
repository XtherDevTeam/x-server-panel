let mainForm = new x_object("xf-body");
function load_sidebar() {
    let vmlist = fetch_json_api('/api?r=vmlist','get');
    mainForm.insert('<div id="sidebar"></div>');
    let temp = new x_object("sidebar");
    temp.setCSS({
        'side': ""
    })
}
function load_all() {
    
}