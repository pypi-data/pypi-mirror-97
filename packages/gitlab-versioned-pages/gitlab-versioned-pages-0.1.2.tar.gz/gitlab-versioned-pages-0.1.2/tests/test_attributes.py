import pytest

import gitlab_versioned_pages


@pytest.mark.parametrize("attribute", ["__version__"])
def test_attribute(attribute):
    assert getattr(gitlab_versioned_pages, attribute)


def test_main():
    import gitlab_versioned_pages

    assert gitlab_versioned_pages
