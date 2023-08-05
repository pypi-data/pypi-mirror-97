from kubernetes import client, config


class K8s:
    def __init__(self):
        """
        Initialize connection to k8s API
        """
        try:
            config.load_incluster_config()
        except config.config_exception.ConfigException:
            config.load_kube_config()

        self.client = client.CoreV1Api()
        self.batch_api = client.BatchV1Api()
        self.batch_v1beta1_api = client.BatchV1beta1Api()
        self.extension_api = client.ExtensionsV1beta1Api()

    def get_namespace_pods(self, namespace="default", label_selector=""):
        """
        This will return a list of objects req namespace
        """
        return self.client.list_namespaced_pod(
            namespace=namespace, label_selector=label_selector
        )
