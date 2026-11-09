# Changelog

## [0.2.0] — 2026-11-08

### Added
- `dc.py`: DC three-constituent decomposition (DC_disc, DC_prof, DC_comp) with weights, per §3.2.3 of the revised paper.
- `triggers.py`: ECA trigger sets T_ped and T_safety, per §3.8.
- `daemons.py`: Governance trajectory daemons d_dual-prep, d_ethics, d_transparency, per §5.3.
- `embeddings.py`: E_learner, E_action, E_artefact protocol interfaces, per §3.2.2.
- `hybrid.py`: HybridDynamics, empirical_lipschitz, check_theorem_3_1_assumptions, per §3.9.
- `free_energy.py`: PrecisionPrior, ethical_precision, variational_free_energy, per §4.2.1.
- `ethical_competence_via_precision` in `ethical.py`, per §4.2.1.
- `tests/test_dc.py`, `test_triggers.py`, `test_daemons.py`, `test_embeddings.py`, `test_hybrid.py`, `test_free_energy.py`.
- `examples/v02_new_features.py`.

### Changed
- `LearnerState.DC` now returns three-constituent composite (§3.2.3). `DC_decomposed` added for diagnostics. **Breaking** for code relying on the old single-number DC value.
- `__init__.py` exports 25 new symbols; version bumped to 0.2.0.

### Deprecated
- `governance.is_admissible` and `filter_admissible`: superseded by `daemons.GovernanceDaemons` (§5.1). Retained for backward compatibility with a DeprecationWarning.

### Fixed
- `ethical.py` docstring distinguishes competency "ethical judgment" (in DC_comp) from construct EC (§3.2.3).
- All module docstrings now cite section numbers of the revised paper.

## [0.1.0] — 2026-10-01
Initial implementation: capacities, state, ethical competence, flourishing, success, safety gap, SCAM, COH, trajectories, agents, FCP, calibration, experiments.
