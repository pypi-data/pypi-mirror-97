import inflect


def test_an():
    p = inflect.engine()

    assert p.an("cat") == "a cat"
    assert p.an("ant") == "an ant"
    assert p.an("a") == "an a"
    assert p.an("b") == "a b"
    assert p.an("honest cat") == "an honest cat"
    assert p.an("dishonest cat") == "a dishonest cat"
    assert p.an("Honolulu sunset") == "a Honolulu sunset"
    assert p.an("mpeg") == "an mpeg"
    assert p.an("onetime holiday") == "a onetime holiday"
    assert p.an("Ugandan person") == "a Ugandan person"
    assert p.an("Ukranian person") == "a Ukranian person"
    assert p.an("Unabomber") == "a Unabomber"
    assert p.an("unanimous decision") == "a unanimous decision"
    assert p.an("US farmer") == "a US farmer"
    assert p.an("wild PIKACHU appeared") == "a wild PIKACHU appeared"
