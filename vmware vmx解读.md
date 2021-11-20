### 不可更改

```ini
pciBridge0.present = "TRUE"
pciBridge4.present = "TRUE"
pciBridge4.virtualDev = "pcieRootPort"
pciBridge4.functions = "8"
pciBridge5.present = "TRUE"
pciBridge5.virtualDev = "pcieRootPort"
pciBridge5.functions = "8"
pciBridge6.present = "TRUE"
pciBridge6.virtualDev = "pcieRootPort"
pciBridge6.functions = "8"
pciBridge7.present = "TRUE"
pciBridge7.virtualDev = "pcieRootPort"
pciBridge7.functions = "8"
pciBridge0.pciSlotNumber = "17"
pciBridge4.pciSlotNumber = "21"
pciBridge5.pciSlotNumber = "22"
pciBridge6.pciSlotNumber = "23"
pciBridge7.pciSlotNumber = "24"

vmci0.present = "TRUE"
vmci0.pciSlotNumber = "36"
vmci0.id = "1031424121"

virtualHW.productCompatibility = "hosted"

powerType.powerOff = "soft"
powerType.powerOn = "soft"
powerType.suspend = "soft"
powerType.reset = "soft"

cleanShutdown = "FALSE"
softPowerOff = "FALSE"

usb.vbluetooth.startConnected = "TRUE"
sensor.location = "pass-through"
.encoding = "UTF-8"
config.version = "8"
virtualHW.version = "19"

usb.present = "TRUE"
usb.pciSlotNumber = "32"

usb:1.speed = "2"
usb:1.present = "TRUE"
usb:1.deviceType = "hub"
usb:1.port = "1"
usb:1.parent = "-1"

ehci.present = "TRUE"
ehci.pciSlotNumber = "35"

usb_xhci.present = "TRUE"
usb_xhci:4.present = "TRUE"
usb_xhci:4.deviceType = "hid"
usb_xhci:4.port = "4"
usb_xhci:4.parent = "-1"
```

### Remote controlling

```ini
RemoteDisplay.vnc.enabled = "TRUE"
RemoteDisplay.vnc.port = "5902"
```

### Sound card

```ini
sound.startConnected = "FALSE"
sound.autoDetect = "TRUE"
sound.virtualDev = "hdaudio"
sound.fileName = "-1"
sound.present = "TRUE"
sound.pciSlotNumber = "34"
```

### CPU Cores

```ini
numvcpus = "vcpu count"
cpuid.coresPerSocket = "vcpu count"
```

### Memory

```ini
memsize = "memsize"
mem.hotadd = "TRUE" # Recommend this option
```

### SATA Controller

增加设备只需要增加`Devices(type)`那一项的vmx配置即可

```ini
# Controller
sata[n].present = "TRUE" # persent controller
sata[n].pciSlotNumber = "37 + [n]"

# Devices(Harddisk)
sata[n]:[n`].fileName = "path to vmdk file"
sata[n]:[n`].present = "TRUE"
sata[n]:[n`].redo = ""

# Devices(CDROM)
sata[n]:[n`].deviceType = "cdrom-raw"
sata[n]:[n`].fileName = "path to iso file"
sata[n]:[n`].present = "TRUE"
```

### Ethernet

```ini
ethernet0.connectionType = "nat"
ethernet0.addressType = "generated"
ethernet0.virtualDev = "e1000e"
ethernet0.present = "TRUE"
ethernet0.pciSlotNumber = "33"
ethernet0.generatedAddress = "00:0c:29:69:6c:fa" # configure by your self
ethernet0.generatedAddressOffset = "0"
```

### Graphics

```ini
mks.enable3d = "TRUE or FALSE"
svga.graphicsMemoryKB = "8388608"
svga.vramSize = "268435456"

monitor.phys_bits_used = "45"

vmotion.checkpointFBSize = "4194304"
vmotion.checkpointSVGAPrimarySize = "268435456"
vmotion.svga.mobMaxSize = "1073741824"
vmotion.svga.graphicsMemoryKB = "8388608" # follow svga.graphicsMemoryKB
vmotion.svga.supports3D = "1" # Can configure to 0
vmotion.svga.baseCapsLevel = "9"
vmotion.svga.maxPointSize = "189"
vmotion.svga.maxTextureSize = "16384"
vmotion.svga.maxVolumeExtent = "2048"
vmotion.svga.maxTextureAnisotropy = "2"
vmotion.svga.lineStipple = "1"
vmotion.svga.dxMaxConstantBuffers = "14"
vmotion.svga.dxProvokingVertex = "1"
vmotion.svga.sm41 = "1"
vmotion.svga.multisample2x = "1"
vmotion.svga.multisample4x = "1"
vmotion.svga.msFullQuality = "1"
vmotion.svga.logicOps = "1"
vmotion.svga.bc67 = "9"
vmotion.svga.sm5 = "1"
vmotion.svga.multisample8x = "1"
vmotion.svga.logicBlendOps = "1"
```

### 需要修改的项目

```ini
nvram = "path to nvram"
displayName = "vm name"
firmware = "efi or bios"
uefi.secureBoot.enabled = "TRUE or FALSE"
guestOS = "windows9-64 or any"
tools.syncTime = "FALSE or TRUE"
extendedConfigFile = "path to extended vm config file"
```