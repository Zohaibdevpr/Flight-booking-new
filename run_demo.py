"""
Quick demo runner for all SOLID principles.

Run this file to see demonstrations of all SOLID principles:
- SRP: Single Responsibility Principle
- OCP: Open/Closed Principle
- LSP: Liskov Substitution Principle
- ISP: Interface Segregation Principle
- DIP: Dependency Inversion Principle

Usage:
    python run_demo.py [principle]
    
Examples:
    python run_demo.py                 # Run all demos
    python run_demo.py srp             # Run only SRP demo
    python run_demo.py ocp             # Run only OCP demo
    python run_demo.py lsp             # Run only LSP demo
    python run_demo.py isp             # Run only ISP demo
    python run_demo.py dip             # Run only DIP demo
"""

import sys
from examples.demo_srp import demo_srp
from examples.demo_ocp import demo_ocp
from examples.demo_lsp import demo_lsp
from examples.demo_isp import demo_isp
from examples.demo_dip import demo_dip


def run_all_demos():
    """Run all SOLID principle demos."""
    print("\n")
    print("=" * 80)
    print("FLIGHT BOOKING SYSTEM - SOLID PRINCIPLES DEMONSTRATION")
    print("=" * 80)

    try:
        print("\n[1/5] Running SRP Demo...")
        demo_srp()

        print("\n[2/5] Running OCP Demo...")
        demo_ocp()

        print("\n[3/5] Running LSP Demo...")
        demo_lsp()

        print("\n[4/5] Running ISP Demo...")
        demo_isp()

        print("\n[5/5] Running DIP Demo...")
        demo_dip()

        print("\n")
        print("=" * 80)
        print("ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("=" * 80)

    except Exception as e:
        print(f"\n✗ Error running demos: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


def run_specific_demo(principle: str):
    """Run a specific SOLID principle demo."""
    principle = principle.lower()

    demos = {
        "srp": ("Single Responsibility Principle", demo_srp),
        "ocp": ("Open/Closed Principle", demo_ocp),
        "lsp": ("Liskov Substitution Principle", demo_lsp),
        "isp": ("Interface Segregation Principle", demo_isp),
        "dip": ("Dependency Inversion Principle", demo_dip),
    }

    if principle not in demos:
        print(f"Unknown principle: {principle}")
        print(f"Available principles: {', '.join(demos.keys())}")
        sys.exit(1)

    title, demo_func = demos[principle]

    print("\n")
    print("=" * 80)
    print(f"FLIGHT BOOKING SYSTEM - {title.upper()} DEMO")
    print("=" * 80)

    try:
        demo_func()
        print("\n")
        print("=" * 80)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 80)
    except Exception as e:
        print(f"\n✗ Error running demo: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific demo
        principle = sys.argv[1]
        run_specific_demo(principle)
    else:
        # Run all demos
        run_all_demos()
