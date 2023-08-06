from kubernetes import client as k8s

from . import Resource


class ConfigMap(Resource):
    def delete(self, body: k8s.V1DeleteOptions):
        return k8s.CoreV1Api(self.client).delete_namespaced_config_map(
            body=body, namespace=self.namespace, name=self.name
        )

    def create(self):
        return k8s.CoreV1Api(self.client).create_namespaced_config_map(
            body=self.resource, namespace=self.namespace
        )

    def patch(self):
        return k8s.CoreV1Api(self.client).patch_namespaced_config_map(
            name=self.name, body=self.resource, namespace=self.namespace
        )

    def read(self):
        return k8s.CoreV1Api(self.client).read_namespaced_config_map(
            name=self.name, namespace=self.namespace
        )
