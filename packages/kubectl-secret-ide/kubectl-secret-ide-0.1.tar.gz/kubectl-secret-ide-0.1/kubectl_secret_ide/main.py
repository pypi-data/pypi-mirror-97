import base64

from kubernetes import config, client
from simple_term_menu import TerminalMenu


def main() -> None:
    config.load_kube_config()

    v1 = client.CoreV1Api()
    secrets_list: [client.V1Secret] = v1.list_namespaced_secret(namespace="invoicing-test")
    secrets_names = list(map(lambda s: s.metadata.name, secrets_list.items))
    secret = secrets_list.items[TerminalMenu(secrets_names).show()]
    secret_data_keys = list(secret.data.keys())
    secret_data_key = secret_data_keys[TerminalMenu(secret_data_keys).show()]
    secret_data = secret.data[secret_data_key]
    print(secret_data)


if __name__ == '__main__':
    main()
