from scarlet.cms import bundles, views
import pytest


class TestMainBundle(bundles.Bundle):
    navigation = bundles.PARENT
    main = views.ListView(display_fields=("user", "text"))

    class Meta:
        primary_model_bundle = True


class TestBundle1(TestMainBundle):
    navigation = bundles.PARENT

    class Meta:
        primary_model_bundle = True


class TestBundle2(TestMainBundle):
    navigation = bundles.PARENT
    dashboard = (
        ("main",),
        ("tv_main", "Landing Page", {"adm_tv_pk": "tv_main"}),
    )

    class Meta:
        primary_model_bundle = True


class TestBundle3(TestBundle2):
    navigation = bundles.PARENT


@pytest.fixture
def tbm():
    return TestMainBundle(
        name="test-main",
        title="Test main Title",
        title_plural="Test main Titles",
        parent=None,
        attr_on_parent=None,
        site=None,
    )


@pytest.fixture
def tb1():
    return TestBundle1(
        name="test1",
        title="Test1 Title",
        title_plural="Test1 Titles",
        parent=None,
        attr_on_parent=None,
        site=None,
    )


@pytest.fixture
def tb2():
    return TestBundle2(
        name="test2",
        title="Test2 Title",
        title_plural="Test2 Titles",
        parent=None,
        attr_on_parent=None,
        site=None,
    )


@pytest.fixture()
def tb3():
    return TestBundle3(
        name="test2",
        title="Test3 Title",
        title_plural="Test3 Titles",
        parent=None,
        attr_on_parent=None,
        site=None,
    )


def test_bundles(tb1, tb2, tb3, tbm):
    tb1.name = "test1 change"
    assert tb1.name == "test1 change"
    assert tb2.name == "test2"
    assert tbm.name == "test-main"

    tbm.title = "333"
    assert tb1.title == "Test1 Title"
    assert tb2.title == "Test2 Title"
    assert tbm.title == "333"

    tb2.dashboard = (("main"),)
    assert tb1.dashboard == ()
    assert tb2.dashboard == (("main"),)
    assert tbm.dashboard == ()
    assert tb3.dashboard == (
        ("main",),
        ("tv_main", "Landing Page", {"adm_tv_pk": "tv_main"}),
    )

    tb1.dashboard = (
        ("main",),
        ("tv_main", "Landing Page", {"adm_tv_pk": "tv_main"}),
    )
    assert tbm.dashboard == ()
    assert tb1.dashboard == (
        ("main",),
        ("tv_main", "Landing Page", {"adm_tv_pk": "tv_main"}),
    )

    assert tb2.dashboard == (("main"),)
    assert tb3.dashboard == (
        ("main",),
        ("tv_main", "Landing Page", {"adm_tv_pk": "tv_main"}),
    )

    tb3.name = "test3"
    assert tbm.name == "test-main"
    assert tb1.name == "test1 change"
    assert tb2.name == "test2"
    assert tb3.name == "test3"
