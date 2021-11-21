from subprocess import Popen, PIPE, STDOUT
import json,os,backend.config,time,uuid
import shutil

def get_registered_vms() -> list:
    with open(backend.config.config['registered_vm_config_path'],'r+') as file:
        j = json.loads(file.read())
        return j['vmx_path']

def register_vm(vmx:str ) -> bool:
    t = get_registered_vms()
    t.append(vmx)
    with open(backend.config.config['registered_vm_config_path'],'w+') as file:
        file.write(json.dumps({
            'vmx_path': t
        }))
    return True

def unregister_vm(vmx:str ) -> bool:
    a = get_registered_vms()
    if a.count(vmx) == 0:
        print(vmx, ' not in list')
        return False
    del a[a.index(vmx)]
    with open(backend.config.config['registered_vm_config_path'],'w+') as file:
        file.write(json.dumps({
            'vmx_path': a
        }))
    return True

def remove_vm(vmx:str ) -> bool:
    try:
        path = os.path.dirname(os.path.abspath(vmx))
        shutil.rmtree(path)
    except Exception as e:
        print(e)
        return False
    return unregister_vm(vmx)

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

def get_cdrom_media(vmx:dict) -> tuple:
    j = 0
    i = 0
    while vmx.get('sata' + str(i) + '.present') == 'TRUE':
        while vmx.get('sata' + str(i) + ':' + str(j) + '.present') != None: 
            print(vmx.get('sata' + str(i) + ':' + str(j) + '.deviceType'),i,j)
            if vmx.get('sata' + str(i) + ':' + str(j) + '.deviceType') != None and vmx.get('sata' + str(i) + ':' + str(j) + '.deviceType').startswith('cdrom'):
                return (i,j,vmx.get('sata' + str(i) + ':' + str(j) + '.fileName'))
            j = j + 1
        i = i + 1
    return (114,514,"")

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
        'remoteDisplayPort': readResult.get('RemoteDisplay.vnc.port'),
        'cdrom-media': get_cdrom_media(readResult)[2],
        'cdrom-slot': [get_cdrom_media(readResult)[i] for i in range(2)]
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
    handle = Popen("vmware-vdiskmanager -c -s %s -a %s -t 0 \"%s\"" % (size,adapter,vmdk_path), shell=True, stdin=PIPE, stdout=PIPE)
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
            if result.get('.encoding') != None: break
            result[split_result[0]] = split_result[1][1:-1]

    with open(vmx_path, 'r+', encoding=result['.encoding']) as file:
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

def present_sound_card(vmx:dict) -> dict:
    vmx['sound.startConnected'] = "FALSE"
    vmx['sound.autoDetect'] = "TRUE"
    vmx['sound.virtualDev'] = "hdaudio"
    vmx['sound.fileName'] = "-1"
    vmx['sound.present'] = "TRUE"
    vmx['sound.pciSlotNumber'] = "34"
    return vmx

def present_sata_controller(vmx:dict, n:int) -> dict:
    vmx['sata' + str(n) + '.present'] = "TRUE"
    vmx['sata' + str(n) + '.pciSlotNumber'] = str(37 + n)
    return vmx
    
def get_free_sata_slot(vmx:dict, controller:int) -> int:
    j = 0
    while vmx.get('sata' + str(controller) + ':' + str(j) + '.present') == "TRUE": j = j + 1
    return j

def present_sata_harddisk(vmx:dict, vmdk:str, controller: int) -> dict:
    j = get_free_sata_slot(vmx,controller)
    vmx['sata' + str(controller) + ':' + str(j) + '.present'] = "TRUE"
    vmx['sata' + str(controller) + ':' + str(j) + '.fileName'] = vmdk
    vmx['sata' + str(controller) + ':' + str(j) + '.redo'] = ''
    return vmx

def present_sata_cdrom(vmx:dict, iso:str, controller:int) -> dict:
    j = get_free_sata_slot(vmx,controller)
    vmx['sata' + str(controller) + ':' + str(j) + '.present'] = "TRUE"
    vmx['sata' + str(controller) + ':' + str(j) + '.deviceType'] = "cdrom-image"
    vmx['sata' + str(controller) + ':' + str(j) + '.fileName'] = iso
    return vmx

def setup_sata_cdrom(vmx:dict, iso:str, controller:int, slot:int) -> dict:
    if vmx.get('sata' + str(controller) + ':' + str(slot) + '.present') != None:
        vmx['sata' + str(controller) + ':' + str(slot) + '.present'] = "TRUE"
        vmx['sata' + str(controller) + ':' + str(slot) + '.deviceType'] = "cdrom-image"
        vmx['sata' + str(controller) + ':' + str(slot) + '.fileName'] = iso
    return vmx

def set_cdrom_media(vmx:str, iso:str) -> bool:
    v = vmx_read(vmx)
    # controller: int, slot: int
    controller = get_cdrom_media(v)[0]
    slot = get_cdrom_media(v)[1]
    setup_sata_cdrom(v,iso,controller,slot)
    return vmx_write(vmx,v)

def remove_sata_slot(vmx:dict, controller: int, j: int) -> dict:
    j = str(j)
    if vmx.get('sata' + str(controller) + ':' + j + '.present') != None:
        del vmx['sata' + str(controller) + ':' + j + '.present']
    if vmx.get('sata' + str(controller) + ':' + j + '.deviceType') != None:
        del vmx['sata' + str(controller) + ':' + j + '.deviceType']
    if vmx.get('sata' + str(controller) + ':' + j + '.fileName') != None:
        del vmx['sata' + str(controller) + ':' + j + '.fileName']
    if vmx.get('sata' + str(controller) + ':' + j + '.redo') != None:
        del vmx['sata' + str(controller) + ':' + j + '.redo']
    return vmx

def present_network(vmx:dict) -> dict:
    vmx['ethernet0.connectionType'] = "nat"
    vmx['ethernet0.addressType'] = "generated"
    vmx['ethernet0.virtualDev'] = "e1000e"
    vmx['ethernet0.present'] = "TRUE"
    vmx['ethernet0.pciSlotNumber'] = "33"
    vmx['ethernet0.generatedAddress'] = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    vmx['ethernet0.generatedAddressOffset'] = "0"
    return vmx

def presentVideo(vmx:dict) -> dict:
    vmx['mks.enable3d'] = "TRUE"
    vmx['svga.graphicsMemoryKB'] = "8388608"
    vmx['svga.vramSize'] = "268435456"

    vmx['monitor.phys_bits_used'] = "45"

    vmx['vmotion.checkpointFBSize'] = "4194304"
    vmx['vmotion.checkpointSVGAPrimarySize'] = "268435456"
    vmx['vmotion.svga.mobMaxSize'] = "1073741824"
    vmx['vmotion.svga.graphicsMemoryKB'] = vmx['svga.graphicsMemoryKB'] # follow svga.graphicsMemoryKB
    vmx['vmotion.svga.supports3D'] = "1" # Can configure to 0
    vmx['vmotion.svga.baseCapsLevel'] = "9"
    vmx['vmotion.svga.maxPointSize'] = "189"
    vmx['vmotion.svga.maxTextureSize'] = "16384"
    vmx['vmotion.svga.maxVolumeExtent'] = "2048"
    vmx['vmotion.svga.maxTextureAnisotropy'] = "2"
    vmx['vmotion.svga.lineStipple'] = "1"
    vmx['vmotion.svga.dxMaxConstantBuffers'] = "14"
    vmx['vmotion.svga.dxProvokingVertex'] = "1"
    vmx['vmotion.svga.sm41'] = "1"
    vmx['vmotion.svga.multisample2x'] = "1"
    vmx['vmotion.svga.multisample4x'] = "1"
    vmx['vmotion.svga.msFullQuality'] = "1"
    vmx['vmotion.svga.logicOps'] = "1"
    vmx['vmotion.svga.bc67'] = "9"
    vmx['vmotion.svga.sm5'] = "1"
    vmx['vmotion.svga.multisample8x'] = "1"
    vmx['vmotion.svga.logicBlendOps'] = "1"
    return vmx

def set_cpu_cores(vmx: dict,cores: int = 2) -> dict:
    vmx['numvcpus'] = str(cores)
    vmx['cpuid.coresPerSocket'] = str(cores)
    return vmx

def set_mem_size(vmx: dict,size: int = 2048) -> dict:
    vmx['memsize'] = str(size)
    vmx['mem.hotadd'] = "TRUE"
    return vmx

def create_vm(vm_name: str, guestOS:str, remote_port: int, cpu_cores:int, memsize:int, root_disk_size: str, ) -> bool:
    path = backend.config.config['new_vm_default_path'] + '/' + vm_name
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
    
    vmx['guestOS'] = guestOS

    vmx['nvram'] = 'host.nvram'
    
    vmx['displayName'] = vm_name

    present_network(vmx)
    present_sound_card(vmx)
    set_cpu_cores(vmx, cpu_cores)
    set_mem_size(vmx, memsize)
    create_vdisk(root_disk_size, 'lsilogic', path + '/' + 'main.vmdk')
    present_sata_controller(vmx, 0)
    present_sata_harddisk(vmx, 'main.vmdk', 0)
    presentVideo(vmx)
    present_sata_cdrom(vmx, '/dev/cdrom', 0)
    
    if vmx_write(path + '/' + vm_name + '.vmx',vmx):
        return register_vm(path + '/' + vm_name + '.vmx')
    else: return False
