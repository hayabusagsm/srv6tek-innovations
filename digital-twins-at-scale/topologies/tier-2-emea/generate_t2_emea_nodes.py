#!/usr/bin/env python3
"""
SRv6TEK Innovations - Tier-2-EMEA Node Schema Generator
Automates Containerlab node mappings using Deutsche Telekom AS3320.
"""

def build_emea_nodes(layout_strategy="vendor-mix"):
    # Authoritative EMEA Carrier Hotel Geographical Database
    pop_geo = {
        1: "london_telehouse", 2: "slough_equinix", 3: "frankfurt_interxion", 4: "amsterdam_nikhef",
        5: "paris_voltaire", 6: "marseille_interxion", 7: "palermo_sparkle", 8: "madrid_interxion",
        9: "dublin_equinix", 10: "zurich_interxion", 11: "milan_caldera", 12: "vienna_interxion",
        13: "stockholm_equinix", 14: "copenhagen_interxion", 15: "warsaw_lim", 16: "istanbul_equinix",
        17: "athens_lamda", 18: "lisbon_sines", 19: "helsinki_equinix", 20: "dubai_dx1",
        21: "riyadh_center3", 22: "cape_town_teraco", 23: "johannesburg_teraco"
    }
    
    asn = "3320"
    yaml_out = ["# ==============================================================================",
                f"# PROGRAMMATIC NODE MATRIX FOR TIER-2-EMEA | CARRIER: DEUTSCHE TELEKOM (AS{asn})",
                "# ==============================================================================\n  nodes:"]

    for r in range(1, 135):
        node_id = f"R{r}"
        pop_idx = ((r - 1) // 4) + 1 if r <= 92 else 1
        pop_name = pop_geo.get(pop_idx, "backbone_cushion")

        if layout_strategy == "all-cisco":
            kind = "cisco_xrd"
        elif layout_strategy == "all-juniper":
            kind = "juniper_crpd"
        else: # "vendor-mix" -> Splits local environments cleanly
            kind = "cisco_xrd" if pop_idx <= 12 or r > 92 else "juniper_crpd"

        if 1 <= r <= 94:
            role = "P" if (r - 1) % 4 < 2 else "PE"
            node_asn = asn
        elif 95 <= r <= 107:
            role, kind = "RR", ("juniper_crpd" if layout_strategy == "all-juniper" else "cisco_xrd")
            node_asn = asn
        else:
            role, kind = "CE", "linux"
            node_asn = f"65{str(r).zfill(3)}"

        yaml_out.append(f"    {node_id}: {{ kind: {kind}, labels: {{ pop: {pop_name}, role: {role}, as: \"{node_asn}\" }} }}")

    with open("nodes.yaml", "w") as f:
        f.write("\n".join(yaml_out) + "\n")
    print(f"🟢 Generated Tier-2-EMEA nodes.yaml using layout: {layout_strategy}")

if __name__ == "__main__":
    build_emea_nodes(layout_strategy="vendor-mix")
