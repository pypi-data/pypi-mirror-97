import pytest

from insnail_ai_tools.config import ApolloConfig, YamlConfig


def test_apollo_config():
    class Config(ApolloConfig):
        MONGO_URI: str = None

    config = Config(
        "insnail-qa-robot",
        "http://10.0.0.176:8080",
        "default",
    )
    config.fetch()
    assert bool(config.MONGO_URI) is True


def test_yaml_config():
    class Config(YamlConfig):
        MONGO_URI: str = None

    config = Config("./tests/test_config.yaml")
    config.fetch()
    assert config.MONGO_URI == "mongo_uri"
