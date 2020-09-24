from ctypes import *
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
lib = cdll.LoadLibrary(os.path.join(dir_path, "hw.so"))

lib.install.restype = c_char_p
lib.upgrade.restype = c_char_p
lib.uninstall.restype = c_char_p

class STATUS(Structure):
    _fields_ = [("res", c_char_p),
                ("status", c_int)]

lib.get_status.restype = STATUS

def get_status(name, namespace, kubeconfig):
    STATUS = lib.get_status(name.encode('utf-8'),
                         namespace.encode('utf-8'),
                         kubeconfig.encode('utf-8'))
    return STATUS.res.decode("utf-8"), STATUS.status

def install_chart(chartPath, releaseName, vals, namespace, kubeconfig):
    res = lib.install(chartPath.encode('utf-8'),
                      releaseName.encode('utf-8'),
                      vals.encode('utf-8'),
                      namespace.encode('utf-8'),
                      kubeconfig.encode('utf-8'))
    return res.decode("utf-8")

def upgrade_chart(chartPath, releaseName, vals, namespace, kubeconfig):
    res = lib.upgrade(chartPath.encode('utf-8'),
                      releaseName.encode('utf-8'),
                      vals.encode('utf-8'),
                      namespace.encode('utf-8'),
                      kubeconfig.encode('utf-8'))
    return res.decode("utf-8")

def uninstall_chart(releaseName, namespace, kubeconfig):
    res = lib.uninstall(releaseName.encode('utf-8'),
                        namespace.encode('utf-8'),
                        kubeconfig.encode('utf-8'))
    return res.decode("utf-8")

if __name__ == '__main__':
    namespace = 'test-ns'
    kubeconfig = '/Users/stefan/stackn-deployments/snic-iscl/config'


    vals = ('labs.resources.limits.cpu=1000m,'
            'labs.resources.limits.mem=1Gi')

    chartPath = '/Users/stefan/scaleout-dev/charts/scaleout/lab'
    releaseName = 'test-rel'

    res = install_chart(chartPath, releaseName, vals, namespace, kubeconfig)
    print(res)
    res, status = get_status(releaseName, 'default', kubeconfig)
    if status==0:
        print("Failed to fetch status of release")
    print(res)
    vals = ('labs.resources.limits.cpu=500m,'
            'labs.resources.limits.mem=1Gi')
    res = upgrade_chart(chartPath, releaseName, vals, namespace, kubeconfig)
    print(res)
    res = get_status(releaseName, namespace, kubeconfig)
    print(res)
    res = uninstall_chart(releaseName, namespace, kubeconfig)
    print(res)