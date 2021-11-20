let mount_point = "xfrontend_mount_point";

class x_object{
    constructor(node_id){
        this.dom = document.getElementById(node_id);
    }

    insert(html){
        this.dom.innerHTML += html;
    }

    remove(id){
        this.dom.getElementById(id).remove();
    }

    remove_self(){
        this.dom.remove();
    }

    setCSS(json){
        let build = "";
        for (const key in json) {
            if (Object.hasOwnProperty.call(json, key)) {
                const element = json[key];
                build += key + ": " + element + ';';
            }
        }
        this.dom.setAttribute("style",build);
    }

    setClassList(clist){
        this.dom.setAttribute("class","");
        clist.forEach(element => {
            this.dom.classList.add(element)
        });
    }

    setHtml(html){
        this.dom.innerHTML = html;
    }

    getHtml(){
        return this.dom.innerHTML;
    }
};

function m(node_id){
    return new x_object(node_id);
}

function fetch_json_api_nosync(url,method,callback){
    if(method == undefined) method = 'get';
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.open(method,url,1);
    xmlhttp.onload = () => {
        callback(JSON.parse(xmlhttp.responseText));
    };
    xmlhttp.send();
}

function fetch_json_api(url,method){
    if(method == undefined) method = 'get';
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.open(method,url,0);
    xmlhttp.send();
    try {
        let result = JSON.parse(xmlhttp.responseText);
        return result;
    } catch (error) {
        return null;
    }
}

function arg(name) {
    let reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    let r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return decodeURIComponent(r[2]);
    };
    return null;
 }