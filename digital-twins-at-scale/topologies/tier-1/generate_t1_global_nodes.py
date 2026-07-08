#!/usr/bin/env python3
"""
SRv6TEK Innovations - Tier-1 Global Core Node Schema Generator
Slices core infrastructure into separate corporate identities: AS701, AS702, AS703.
"""

def build_t1_nodes(layout_strategy="vendor-mix"):
    yaml_out = ["# ==============================================================================",
                "# PROGRAMMATIC NODE MATRIX FOR TIER-1 GLOBAL CORES (AS701 / AS702 / AS703)",
                "# ==============================================================================\n  nodes:"]

    for r in range(1, 135):
        node_id = f"R{r}"
        pop_idx = ((r - 1) // 4) + 1 if r <= 92 else 1

        # Multi-AS Infrastructure Slicing Boundaries
        if 1 <= r <= 46:
            asn, pop_zone = "701", "us_transit_zone"
        elif 47 <= r <= 70:
            asn, pop_zone = "702", "emea_transit_zone"
        elif 71 <= r <= 107:
            asn, pop_zone = "703", "apac_transit_zone"
        else:
            asn, pop_zone = f"65{str(r).zfill(3)}", "customer_edge_zone"

        # Platform Deployment Logic
        if layout_strategy == "all-cisco":
            kind = "cisco_xrd"
        elif layout_strategy == "all-juniper":
            kind = "juniper_crpd"
        else:
            kind = "cisco_xrd" if pop_idx <= 12 or r > 92 else "juniper_crpd"

        # Assign Specific Functional Roles
        if 1 <= r <= 94:
            role = "P" if (r - 1) % 4 < 2 else "PE"
            node_asn = asn
        elif 95 <= r <= 107:
            role, kind = "RR", ("juniper_crpd" if layout_strategy == "all-juniper" else "cisco_xrd")
            node_asn = asn
        else:
            role, kind = "CE", "linux"
            node_asn = asn

        yaml_out.append(f"    {node_id}: {{ kind: {kind}, labels: {{ zone: {pop_zone}, role: {role}, as: \"{node_asn}\" }} }}")

    with open("nodes.yaml", "w") as f:
        f.write("\n".join(yaml_out) + "\n")
    print(f"🟢 Generated Tier-1 Global Core nodes.yaml using layout: {layout_strategy}")

if __name__ == "__main__":
    build_t1_nodes(layout_strategy="vendor-mix")
