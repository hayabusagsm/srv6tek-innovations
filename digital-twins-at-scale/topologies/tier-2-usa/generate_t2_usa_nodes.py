#!/usr/bin/env python3
"""
SRv6TEK Innovations - Tier-2-USA Node Schema Generator
Automates Containerlab node mappings using Comcast AS11427.
"""

def build_usa_nodes(layout_strategy="vendor-mix"):
    # Official US Carrier Hotel Geographical Database
    pop_geo = {
        1: "ashburn_equinix", 2: "ny_60hudson", 3: "boston_1summer", 4: "newark_165halsey",
        5: "atlanta_56marietta", 6: "miami_nap", 7: "jax_421church", 8: "chicago_350cermak",
        9: "cleveland_rockwell", 10: "dallas_infomart", 11: "houston_fannin", 12: "kc_1102grand",
        13: "minneapolis_511ave", 14: "denver_91015th", 15: "slc_shepard", 16: "phoenix_vanburen",
        17: "la_onewilshire", 18: "sanjose_sv1", 19: "seattle_westin", 20: "hillsboro_flex",
        21: "toronto_151front", 22: "montreal_1250rene", 23: "sandiego_tijuana"
    }
    
    asn = "11427"
    yaml_out = ["# ==============================================================================",
                f"# PROGRAMMATIC NODE MATRIX FOR TIER-2-USA | CARRIER: COMCAST (AS{asn})",
                "# ==============================================================================\n  nodes:"]

    for r in range(1, 135):
        node_id = f"R{r}"
        pop_idx = ((r - 1) // 4) + 1 if r <= 92 else 1
        pop_name = pop_geo.get(pop_idx, "backbone_cushion")

        # Dynamic Platform Vendor Assignment
        if layout_strategy == "all-cisco":
            kind = "cisco_xrd"
        elif layout_strategy == "all-juniper":
            kind = "juniper_crpd"
        else: # "vendor-mix" -> POPs 1-12 Cisco, 13-23 Juniper
            kind = "cisco_xrd" if pop_idx <= 12 or r > 92 else "juniper_crpd"

        # Structural Role Identifiers
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
    print(f"🟢 Generated Tier-2-USA nodes.yaml using layout: {layout_strategy}")

if __name__ == "__main__":
    build_usa_nodes(layout_strategy="vendor-mix")
