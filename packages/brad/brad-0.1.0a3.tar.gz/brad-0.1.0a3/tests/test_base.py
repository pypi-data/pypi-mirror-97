import pytest

from brad.samplers import Sampler


def test_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Sampler(0)
