"""Tests confirming the deprecation of pointwise filter (Section 5.1)."""

import pytest
from ctehf_ai import is_admissible, PedagogicalAction, ActionType


def test_is_admissible_deprecated():
    with pytest.warns(DeprecationWarning):
        a = PedagogicalAction(action_type=ActionType.REFLECT)
        is_admissible(a)
