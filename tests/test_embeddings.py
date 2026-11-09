"""Tests for embedding interfaces (Section 3.2.2)."""

import numpy as np
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    PedagogicalAction, ActionType,
    IdentityLearnerEmbedding, IdentityActionEmbedding, MeanArtefactEmbedding,
    similarity_in_H, nearest_neighbours,
)


def _state(level=0.5):
    return LearnerState(invisible={c: level for c in InvisibleCapacity})


def test_learner_embedding():
    emb = IdentityLearnerEmbedding()
    v = emb(_state(0.5))
    assert v.shape == (10,)
    assert np.all(v == 0.5)


def test_action_embedding():
    emb = IdentityActionEmbedding()
    v = emb(PedagogicalAction(action_type=ActionType.SCAFFOLD))
    assert v.shape == (4,)
    assert v.sum() == 1.0


def test_similarity_identical():
    a = np.array([1.0, 2.0, 3.0])
    assert similarity_in_H(a, a) == 0.0


def test_nearest_neighbours():
    emb = IdentityLearnerEmbedding()
    q = emb(_state(0.5))
    cands = {"a": emb(_state(0.51)), "b": emb(_state(0.9))}
    result = nearest_neighbours(q, cands, delta=0.2)
    assert "a" in result
    assert "b" not in result


def test_mean_artefact():
    emb = MeanArtefactEmbedding()
    v = emb({"a": np.array([1.0, 2.0]), "b": np.array([3.0, 4.0])})
    assert np.allclose(v, [2.0, 3.0])
