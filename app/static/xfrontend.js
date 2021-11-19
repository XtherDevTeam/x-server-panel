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
                build += key + ": " + JSON.stringify(element);
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

function mount_dom(node_id) {
    mount_point = node_id;
    if (document.getElementById(node_id) == null) {
        console.error("mount point not exist.");
    }
    return document.getElementById(node_id);
}

function fetch_json_api(url,method){
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
