from pollination.dragonfly_energy.translate import ModelToHoneybee
from queenbee.plugin.function import Function


def test_model_to_honeybee():
    function = ModelToHoneybee().queenbee
    assert function.name == 'model-to-honeybee'
    assert isinstance(function, Function)
