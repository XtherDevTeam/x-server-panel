let mount_point = "xfrontend_mount_point";

class x_object{
    constructor(node_id){
        if(node_id == null || node_id == undefined){return;}
        this.dom = document.getElementById(node_id);
    }

    insert(html){
        this.dom.innerHTML += html;
    }

    inserts(htmls){
        htmls.forEach(element => {
            this.dom.innerHTML += element + '<br>';
        });
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

    setValue(value){
        this.dom.value = value;
    }

    getValue(){
        return this.dom.value;
    }

    setHtml(html){
        this.dom.innerHTML = html;
    }

    getHtml(){
        return this.dom.innerHTML;
    }

    makeDirectorySelector(showText,name){
        this.dom.innerHTML += "<h5>" + showText + "</h5>";
        this.dom.innerHTML += '<input name="' + name + '" style="width: 80%;display: inline-block;" type="text" class="x-object-path-input form-control" onFocus="path_input_onFocus(this)" oninput="path_input_onchange(this)" />&nbsp;&nbsp;';
        this.dom.innerHTML += '<a class="btn btn-primary" href="javascript:;" onclick="path_input_onok(this)">OK</a>';
        this.dom.innerHTML += '<div style="display: none;" class="x-object-path-select" onclick=""></div>';
    }
    
    nextLine(){
        this.dom.innerHTML += '<br>';
    }

    createInput(id,name,type,showText,placeholder){
        let display = '';
        display += '<div class="form-outline">';
        display += '<input class="form-control" name="' + name + '" id="' + id + '" type="' + type + '"/>';
        display += '<label style="left: 0px;" class="form-label" for="' + id + '">' + showText + '</label>';
        display += '</div>'
        this.insert(display);
        if(placeholder != undefined && placeholder != null){
            m(id).dom.setAttribute('placeholder',placeholder);
        }
    }

    createButton(id,text,onclick){
        let display = '<button class="btn btn-primary" onclick="' + onclick + '" id="' + id + '">' + text + '</button>';
        this.insert(display);
    }

    createSpan(text){
        this.dom.innerHTML += '<span>' + text + '</span>';
    }
};

function path_input_onFocus(nodeEle){
    let x = d(nodeEle.parentNode.getElementsByClassName('x-object-path-select')[0]);
    x.setCSS({'display': 'block'});
}

function path_input_onok(nodeEle){
    let x = d(nodeEle.parentNode.getElementsByClassName('x-object-path-select')[0]);
    x.setCSS({'display': 'none'});
}

function path_input_change_path(nodeEle,path){
    console.log(nodeEle.parentNode.parentNode.parentNode)
    let x = d(nodeEle.parentNode.parentNode.parentNode.getElementsByClassName('x-object-path-input')[0]);
    x.dom.value = path;
    path_input_onchange(x.dom);
}

function path_input_onchange(nodeEle){
    console.log(nodeEle);
    let x = d(nodeEle.parentNode.getElementsByClassName('x-object-path-select')[0]);
    fetch_json_api_nosync('/api?r=path&d=search&p=\'' + nodeEle.parentNode.getElementsByClassName('x-object-path-input')[0].value + '\'','get',function (result) {
        x.setHtml('');
        for (let index = 0; index < result.length; index++) {
            const element = result[index];
            if(element['type'] == 'directory'){
                x.insert('<div><i class="fas fa-folder"></i>&nbsp;&nbsp;<a href="javascript:;" onclick="path_input_change_path(this,\'' + element['path'] + '/\')">' + element['name'] + '</a></div>')
            }else{
                x.insert('<div><i class="fas fa-file"></i>&nbsp;&nbsp;<a href="javascript:;" onclick="path_input_change_path(this,\'' + element['path'] + '\')">' + element['name'] + '</a></div>')
            }
        }
    });
}

function m(node_id){
    return new x_object(node_id);
}

function d(dom){
    let obj = new x_object(null);
    obj.dom = dom;
    return obj
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