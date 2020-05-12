from wac import kafka


def test_get_ssl_args_enabled():
    assert kafka.get_ssl_args() == {
        "security_protocol": "SSL",
        "ssl_cafile": "certs/ca.pem",
        "ssl_certfile": "certs/service.cert",
        "ssl_keyfile": "certs/service.key",
    }


def test_get_ssl_args_disabled(monkeypatch):
    monkeypatch.setattr(kafka.config, "KAFKA_USE_SSL", False)
    assert kafka.get_ssl_args() == {}
