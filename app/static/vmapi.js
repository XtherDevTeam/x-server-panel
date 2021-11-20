function vm_operation(vmx_path, action) {
    if(vmx_path[0] != '\'' || vmx_path[0] != '"') vmx_path = '\'' + vmx_path + '\'';
    fetch_json_api_nosync('/api?r=vm&d=' + action + '&p=' + vmx_path,'get',function (result) {
        if(result['status'] == true){
            window.location.reload();
        }else{
            alert('Operate VM Failed!');
            return false;
        }
    });
    setTimeout(function () {
        window.location.reload();
    },5000)
}