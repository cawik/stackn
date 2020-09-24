from celery import shared_task
from django.conf import settings
from .helmlib import pyhelm
import os

volume_root = "/"
if "TELEPRESENCE_ROOT" in os.environ:
    volume_root = os.environ["TELEPRESENCE_ROOT"]
kubeconfig = os.path.join(volume_root, 'app/chartcontroller/.kube/config')

dir_path = os.path.dirname(os.path.realpath(__file__))
chart_path = os.path.join(dir_path, 'charts')
print(chart_path)


# from kubernetes import client, config
# from pathlib import Path
# if settings.EXTERNAL_KUBECONF:
#     config.load_kube_config('cluster.conf')
# else:
#     if 'TELEPRESENCE_ROOT' in os.environ:
#         from kubernetes.config.incluster_config import (SERVICE_CERT_FILENAME,
#                                                   SERVICE_TOKEN_FILENAME,
#                                                   InClusterConfigLoader)

#         token_filename = Path(os.getenv('TELEPRESENCE_ROOT', '/')
#                               ) / Path(SERVICE_TOKEN_FILENAME).relative_to('/')
#         cert_filename = Path(os.getenv('TELEPRESENCE_ROOT', '/')
#                             ) / Path(SERVICE_CERT_FILENAME).relative_to('/')

#         InClusterConfigLoader(
#             token_filename=token_filename, cert_filename=cert_filename
#         ).load_and_set()
#     else:
#         config.load_incluster_config()

# print(dir(config))
# print(dir(config.kube_config))
# print(SERVICE_TOKEN_FILENAME)
# ftoken = open(token_filename, 'r')
# token = ftoken.read()
# print(token)
# fcert = open(cert_filename, 'r')
# cert = fcert.read()
# print(cert)
# print(SERVICE_CERT_FILENAME)

@shared_task
def install_chart(chart, releaseName, vals, namespace):
    # namespace = 'test-ns'
    # kubeconfig = '/Users/stefan/stackn-deployments/snic-iscl/config'


    # vals = ('labs.resources.limits.cpu=1000m,'
    #         'labs.resources.limits.mem=1Gi')

    # chartPath = '/Users/stefan/scaleout-dev/charts/scaleout/lab'
    # releaseName = 'test-rel'
    vals_in = ''
    for key in vals:
        vals_in += key+'='+vals[key]+','
    vals_in = vals_in[0:-1]
    # print(vals_in)
    chartp = os.path.join(chart_path, chart)
    print('creating resources...')
    res = pyhelm.install_chart(chartp, releaseName, vals_in, namespace, kubeconfig)
    print(res)