from subprocess import Popen, PIPE, STDOUT
import json,os,backend.config,time

def get_registered_vms() -> list:
    with open(backend.config.config['registered_vm_config_path'],'r+') as file:
        j = json.loads(file.read())
        return j['vmx_path']

def get_registered_vm_names() -> list:
    with open(backend.config.config['registered_vm_config_path'],'r+') as file:
        j = json.loads(file.read())
        print(j['vmx_path'])
        return [get_vm_name(i) for i in j['vmx_path']]

def get_registered_vm_details() -> list:
    with open(backend.config.config['registered_vm_config_path'],'r+') as file:
        j = json.loads(file.read())
        print(j['vmx_path'])
        return [get_vm_detail(i) for i in j['vmx_path']]

def get_running_vms() -> list:
    handle = Popen("vmrun -T ws list", shell=True, stdin=PIPE, stdout=PIPE)
    handle.wait()
    result = handle.stdout.read().decode('utf-8')
    l = result.splitlines()
    l = l[1:]
    return l

def get_vm_name(vmx_path:str) -> str:
    return vmx_read(vmx_path)['displayName']

def get_vm_detail(vmx_path:str) -> str:
    running = get_running_vms()
    readResult = vmx_read(vmx_path)
    return {
        'name': readResult['displayName'],
        'running': running.count(vmx_path),
        'vmxPath': vmx_path,
        'efi': readResult.get('firmware') != None,
        'guestOS': readResult['guestOS'],
        'enable3d': readResult['mks.enable3d'],
        'graphicsMemory': readResult['svga.graphicsMemoryKB'],
        'macAddr': readResult['ethernet0.generatedAddress'],
        'memSize': readResult['memsize'],
        'core_count': readResult['numvcpus'],
        'remoteDisplay': readResult.get('RemoteDisplay.vnc.enabled') != None and readResult.get('RemoteDisplay.vnc.enabled') == 'TRUE',
        'remoteDisplayPort': readResult.get('RemoteDisplay.vnc.port')
    }

def start_vm(vmx_path:str, ) -> bool:
    handle = Popen("vmrun -T ws start \"%s\" nogui" % vmx_path, shell=True, stdin=PIPE, stdout=PIPE)
    handle.wait(10)
    result = handle.stdout.read().decode('utf-8')
    if result.find('Error') == -1: return True
    print(result)
    return False

def stop_vm(vmx_path:str) -> bool:
    handle = Popen("vmrun -T ws stop \"%s\" hard" % vmx_path, shell=True, stdin=PIPE, stdout=PIPE)
    handle.wait()
    result = handle.stdout.read().decode('utf-8')
    if result == "": return True
    print(result)
    return False

def reset_vm(vmx_path:str, ) -> bool:
    handle = Popen("vmrun -T ws reset \"%s\" hard" % vmx_path, shell=True, stdin=PIPE, stdout=PIPE)
    handle.wait()
    result = handle.stdout.read().decode('utf-8')
    if result.find('Error') == -1: return True
    print(result)
    return False

def suspend_vm(vmx_path:str, ) -> bool:
    handle = Popen("vmrun -T ws suspend \"%s\" hard" % vmx_path, shell=True, stdin=PIPE, stdout=PIPE)
    handle.wait()
    result = handle.stdout.read().decode('utf-8')
    if result.find('Error') == -1: return True
    print(result)
    return False

def create_vdisk(size:str, adapter:str, vmdk_path:str) -> bool:
    handle = Popen("vmware-vdiskmanager -c -s %s -a %s 0 \"%s\"" % (size,adapter,vmdk_path), shell=True, stdin=PIPE, stdout=PIPE)
    handle.wait()
    result = handle.stdout.read().decode('utf-8')
    if result.find('Failed') == -1: return True
    return False

def vmx_read(vmx_path:str) -> dict:
    print(vmx_path)
    result = {}
    with open(vmx_path, 'r+', encoding='gbk') as file:
        for i in file.readlines():
            if i[0] == '#' or i == '\n': continue
            i = i[0:-1]
            split_result = i.split(' = ')
            # print(split_result)
            result[split_result[0]] = split_result[1][1:-1]
        
    return result

def vmx_write(vmx_path:str, data:dict) -> bool:
    try:
        with open(vmx_path,'w+') as file:
            file.write('#!/usr/bin/vmware\n')
            for i in data:
                file.write('%s = "%s"\n' % (i,data[i]))
                
        return True
    except Exception as e:
        return False
    
# @create_nvram
# path -> vm folder path
def create_nvram(path: str) -> bool:
    try:
        with open('backend/template.nvram','rb+') as file:
            with open(path + '/host.nvram', mode='wb+') as toWrite:
                toWrite.write(file.read())
        return True
    except Exception as e:
        print('Error: ',e)
        return False

def present_sound_card(vmx:dict):
    vmx['sound.startConnected'] = "FALSE"
    vmx['sound.autoDetect'] = "TRUE"
    vmx['sound.virtualDev'] = "hdaudio"
    vmx['sound.fileName'] = "-1"
    vmx['sound.present'] = "TRUE"
    vmx['sound.pciSlotNumber'] = "34"
    return vmx

def set_cpu_cores(vmx: dict,cores: int = 2):
    vmx['numvcpus'] = str(cores)
    vmx['cpuid.coresPerSocket'] = str(cores)
    return vmx

def set_mem_size(vmx: dict,size: int = 2048):
    vmx['memsize'] = str(size)
    vmx['mem.hotadd'] = "TRUE"

def create_vm(vm_name: str, guestOS:str, remote_port: int, cpu_cores:int, memsize:int, root_disk_size: str, ) -> bool:
    path = backend.config['new_vm_default_path'] + '/' + vm_name
    os.makedirs(path, mode=0o777, exist_ok=True)
    
    create_nvram(path) 
    
    vmx = {}
    vmx['pciBridge0.present'] = 'TRUE'
    vmx['pciBridge4.present'] = 'TRUE'
    vmx['pciBridge4.virtualDev'] = 'pcieRootPort'
    vmx['pciBridge4.functions'] = "8"
    
    vmx['pciBridge5.present'] = 'TRUE'
    vmx['pciBridge5.virtualDev'] = 'pcieRootPort'
    vmx['pciBridge5.functions'] = "8"
    
    vmx['pciBridge6.present'] = 'TRUE'
    vmx['pciBridge6.virtualDev'] = 'pcieRootPort'
    vmx['pciBridge6.functions'] = "8"
    
    vmx['pciBridge7.present'] = 'TRUE'
    vmx['pciBridge7.virtualDev'] = 'pcieRootPort'
    vmx['pciBridge7.functions'] = "8"
    
    vmx['pciBridge0.pciSlotNumber'] = "17"
    vmx['pciBridge4.pciSlotNumber'] = "21"
    vmx['pciBridge5.pciSlotNumber'] = "22"
    vmx['pciBridge6.pciSlotNumber'] = "23"
    vmx['pciBridge7.pciSlotNumber'] = "24"
    
    vmx['vmci0.present'] = "TRUE"
    vmx['vmci0.pciSlotNumber'] = '36'
    vmx['vmci0.id'] = str(int(time.time()))
    
    vmx['virtualHW.productCompatibility'] = "hosted"
    
    vmx['powerType.poertOff'] = "soft"
    vmx['powerType.powerOn'] = "soft"
    vmx['powerType.suspend'] = "soft"
    vmx['powerType.reset'] = "soft"
    
    vmx['cleanShutdown'] = "FALSE"
    vmx['softPowerOff'] = "FALSE"
    
    vmx['usb.vbluetooth.startConnected'] = "TRUE"
    vmx['sensor.location'] = "pass-through"
    vmx['.encoding'] = 'UTF-8'
    vmx['config.version'] = "8"
    vmx['virtualHW.version'] = "19"
    
    vmx["usb.present"] = "TRUE"
    vmx["usb.pciSlotNumber"] = "32"
    
    vmx["usb:1.speed"] = "2"
    vmx["usb:1.present"] = "TRUE"
    vmx["usb:1.deviceType"] = "hub"
    vmx["usb:1.port"] = "1"
    vmx["usb:1.parent"] = "-1"
    
    vmx["ehci.present"] = "TRUE"
    vmx["ehci.pciSlotNumber"] = "35"
    
    vmx['usb_xhci.present'] = "TRUE"
    vmx['usb_xhci:4.present'] = "TRUE"
    vmx['usb_xhci:4.deviceType'] = "hid"
    vmx['usb_xhci:4.port'] = "4"
    vmx['usb_xhci:4.parent'] = "-1"
    
    vmx['RemoteDisplay.vnc.enabled'] = "TRUE"
    vmx['RemoteDisplay.vnc.port'] = remote_port

    vmx['nvram'] = 'host.nvram'

    present_sound_card(vmx)
    set_cpu_cores(vmx, cpu_cores)
    set_mem_size(vmx, memsize)
    create_vdisk(root_disk_size, 'lsilogic', path + '/' + 'main.vmdk')
    
    pass
