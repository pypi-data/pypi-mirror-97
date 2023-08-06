import pytest

import pandas as pd

from seeq import spy
from seeq.spy.assets import Asset, ItemGroup

from .. import _model


@pytest.mark.unit
def test_circular_reference():
    class Circular_Reference(Asset):
        @Asset.Attribute()
        def Top_of_Circle(self, metadata):
            return self.Bottom_of_Circle()

        @Asset.Attribute()
        def Bottom_of_Circle(self, metadata):
            return self.Top_of_Circle()

    with pytest.raises(RuntimeError, match='circular'):
        spy.assets.build(Circular_Reference, pd.DataFrame([{
            'Build Path': 'Path 1',
            'Build Asset': 'Asset 1'
        }]))


@pytest.mark.unit
def test_do_names_match_criteria():
    assert not _model.do_paths_match_criteria(
        '** >> Wood',
        'North America >> Canada >> Ontario >> Woodstock'
    )
    assert not _model.do_paths_match_criteria(
        '* >> Canada >> O*c >> **',
        'North America >> Canada >> Ontario >> Woodstock'
    )
    assert _model.do_paths_match_criteria(
        '* >> Canada >> O*o >> **',
        'North America >> Canada >> Ontario >> Woodstock'
    )
    assert _model.do_paths_match_criteria(
        '* >> Canada >> Ontar?o >> **',
        'North America >> Canada >> Ontario >> Woodstock'
    )
    assert not _model.do_paths_match_criteria(
        'North America >> Canada >> Nova Scotia >> **',
        'North America >> Canada >> Ontario >> Woodstock'
    )
    assert _model.do_paths_match_criteria(
        'North America >> **',
        'North America >> Canada >> Ontario >> Woodstock'
    )
    assert _model.do_paths_match_criteria(
        '**',
        'North America >> Canada >> Ontario >> Woodstock'
    )
    assert _model.do_paths_match_criteria(
        'North America >> Canada >> Ontario >> **',
        'North America >> Canada >> Ontario >> Woodstock'
    )
    assert _model.do_paths_match_criteria(
        'North America >> Canada >> Ontario >> Woodstock >> **',
        'North America >> Canada >> Ontario >> Woodstock'
    )
    assert _model.do_paths_match_criteria(
        'North America >> ** >> Canada >> ** >> Woodstock',
        'North America >> Canada >> Ontario >> Woodstock'
    )
    assert not _model.do_paths_match_criteria(
        'North America >> ** >> Canada >> ** >> Woodstock',
        'North America >> USA >> New York >> Woodstock'
    )
    assert _model.do_paths_match_criteria(
        'North America >> ** >> Canada >> **',
        'North America >> Canada >> Ontario >> Woodstock'
    )
    assert _model.do_paths_match_criteria(
        'North America >> ** >> Woodstock',
        'North America >> Canada >> Ontario >> Woodstock'
    )
    assert _model.do_paths_match_criteria(
        'North America >> * >> * >> Woodstock',
        'North America >> Canada >> Ontario >> Woodstock'
    )


@pytest.mark.unit
def test_from_picker():
    items = ItemGroup([{
        'Type': 'Scalar',
        'Path': 'North America >> Canada >> Ontario >> Woodstock',
        'Asset': 'College Avenue Secondary School',
        'Name': 'Temperature',
        'Formula': '-3C'
    }, {
        'Type': 'CalculatedSignal',
        'Path': 'North America >> Canada >> Ontario >> Woodstock >> Catholic',
        'Asset': 'St. Marys Secondary School',
        'Name': 'Temperature',
        'Formula': '-1C'
    }, {
        'Type': 'Signal',
        'Path': 'North America >> USA >> New York >> Woodstock',
        'Asset': 'Saugerties Senior High School',
        'Name': 'Temperature',
        'Formula': '5C'
    }])

    picked = items.pick({
        'Path': 'North America >> ** >> Woodstock >> **'
    })
    assert len(picked) == 3

    picked = items.pick({
        'Path': 'North America >> ** >> Woodstock >> **',
        'Asset': '*Secondary*'
    })
    assert len(picked) == 2

    picked = items.pick({
        'Path': 'North America >> ** >> Woodstock >> **',
        'Asset': 'Secondary'
    })
    assert len(picked) == 0

    picked = items.pick({
        'Path': 'North America >> **'
    })
    assert len(picked) == 3

    picked = items.pick({
        'Path': 'North America >> * >> Ontario >> *'
    })
    assert len(picked) == 1

    picked = items.pick({
        'Path': 'North America >> * >> * >> Woodstock'
    })
    assert len(picked) == 2

    picked = items.pick({
        'Path': 'North America >> USA >> * >> Woodstock'
    })
    assert len(picked) == 1

    picked = items.pick({
        'Path': 'North America >> *'
    })
    assert len(picked) == 0

    picked = items.pick({
        'Type': 'Scalar'
    })
    assert len(picked) == 1

    picked = items.pick({
        'Type': 'CalculatedSignal'
    })
    assert len(picked) == 1

    picked = items.pick({
        'Type': 'Signal'
    })
    assert len(picked) == 2
