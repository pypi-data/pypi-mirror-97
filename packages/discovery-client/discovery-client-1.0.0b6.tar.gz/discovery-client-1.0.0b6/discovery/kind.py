from enum import Enum


class Kind(str, Enum):
    DEFAULT: str = ""
    CONNECT_PROXY: str = "connect-proxy"
    MESH_GATEWAY: str = "mesh-gateway"
    TERMINATING_GATEWAY: str = "terminating-gateway"
    INGRESS_GATEWAY: str = "ingress-gateway"
