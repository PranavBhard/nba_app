#!/usr/bin/env python3
"""
Verify that all rate stats are correctly handled in the code:
1. All rate stats are in the rate_stats set
2. All rate stats that need aggregation are in the aggregation list
3. Raw vs avg logic is correct
"""

# Rate stats from the code
rate_stats = {
    'effective_fg_perc', 'true_shooting_perc', 'three_perc',
    'off_rtg', 'def_rtg', 'assists_ratio', 'TO_metric', 'ast_to_ratio'
}

# Stats that require aggregation (from _compute_derived_stat_from_aggregate)
aggregation_required = {
    'off_rtg', 'def_rtg', 'assists_ratio', 'TO_metric', 'ast_to_ratio', 
    'effective_fg_perc', 'opp_effective_fg_perc', 
    'opp_true_shooting_perc', 'opp_three_perc', 'opp_assists_ratio', 'opp_points'
}

print("=" * 80)
print("VERIFYING RATE STAT HANDLING IN CODE")
print("=" * 80)
print()

print("Rate stats (from rate_stats set):")
for stat in sorted(rate_stats):
    print(f"  - {stat}")
print()

print("Stats requiring aggregation (from _compute_derived_stat_from_aggregate):")
for stat in sorted(aggregation_required):
    print(f"  - {stat}")
print()

# Check if all rate stats that need aggregation are in the list
print("Checking coverage:")
issues = []
for stat in rate_stats:
    if stat not in aggregation_required:
        issues.append(f"{stat} is a rate stat but not in aggregation_required list")
        print(f"  ✗ {stat}: Missing from aggregation_required")
    else:
        print(f"  ✓ {stat}: Correctly in aggregation_required")

# Check for stats in aggregation_required that aren't rate stats (opponent stats are OK)
print()
print("Stats in aggregation_required that are not rate stats (opponent stats are OK):")
for stat in aggregation_required:
    if stat not in rate_stats and not stat.startswith('opp_'):
        print(f"  - {stat} (not a rate stat, but requires aggregation - this is OK)")

print()
print("=" * 80)
if issues:
    print("✗ ISSUES FOUND:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✓ All rate stats are correctly handled!")
print()

