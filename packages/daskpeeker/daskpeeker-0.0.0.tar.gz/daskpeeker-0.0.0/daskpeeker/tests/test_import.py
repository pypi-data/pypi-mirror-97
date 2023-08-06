import daskpeeker


def test_version():
    assert isinstance(daskpeeker.__version__, str)
