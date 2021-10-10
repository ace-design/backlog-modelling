#!/usr/bin/env python3
"""
    # Launcher to support ECMFA'22 paper
"""
import sys
import scenarios.scenario_1 as s1
import scenarios.scenario_2 as s2
import scenarios.scenario_3 as s3
import scenarios.scenario_4 as s4
import scenarios.scenario_5 as s5

bindings = {
    'scenario_1': s1.run,
    'scenario_2': s2.run,
    'scenario_3': s3.run,
    'scenario_4': s4.run,
    'scenario_5': s5.run
}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Bad arguments")
    func = bindings.get(sys.argv[1], lambda: print(f"Unknown scenario! {sys.argv[1]}"))
    func()

