# This is replaced during release process.
__version_suffix__ = '132'

APP_NAME = "zalando-kubectl"

KUBECTL_VERSION = "v1.19.6"
KUBECTL_SHA512 = {
    "linux": "89105850409f55f6ee29185f17dce4fcabf6b646a42a38cf9339c21d5113e950e0f032ff533116054ee743a65cc097184e18bd970733696b77745db9baf789ed",
    "darwin": "9ff7ba681dd8e29161099ae1a59957b86c61cc963ef4eca944b75fd56ae3930bbf66f9194f17f0a082b9f006a7a1653ca37d96cc19ec7fba615f010066e9db57",
}

STERN_VERSION = "1.13.1"
STERN_SHA256 = {
    "linux": "04a187334748d521d81ac33e4bb52c481d7123e1244b52e209657ba7f7d7fef8",
    "darwin": "6e8a7c522a5580787405e75e69baa1f075d7fbf53629523951113c6512c5cabb",
}

APP_VERSION = KUBECTL_VERSION + "." + __version_suffix__
