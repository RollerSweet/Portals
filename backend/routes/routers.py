from fastapi import APIRouter
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
user = APIRouter()

@user.get("/test_conn")
async def vCenterConnCheck():
    si = SmartConnect(host="1.1.1.200", user="administrator@vsphere.local", pwd="Ultra123!")
    content = si.RetrieveContent()
    # Get the datacenter and folder to create the VM in
    dc = content.rootFolder.childEntity[0]
    vm_folder = dc.vmFolder
    print(vm_folder)
    Disconnect(si)
    return {vm_folder}
