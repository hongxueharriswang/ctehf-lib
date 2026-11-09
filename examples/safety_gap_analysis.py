"""Compare safety gaps across two curricula."""

from ctehf_ai import safety_gap, interpret_safety_gap


def analyze(name, pairs):
    gaps = [safety_gap(a, i) for a, i in pairs]
    print(f"\n{name}: n={len(gaps)} mean_gap={sum(gaps)/len(gaps):.3f}")
    for i, g in enumerate(gaps):
        print(f"  learner {i}: gap={g:+.3f} [{interpret_safety_gap(g).value}]")


def main():
    analyze("Dual-prep", [(0.82, 0.78), (0.76, 0.73), (0.88, 0.85)])
    analyze("AI-dependent", [(0.90, 0.45), (0.85, 0.50), (0.92, 0.55)])


if __name__ == "__main__":
    main()
