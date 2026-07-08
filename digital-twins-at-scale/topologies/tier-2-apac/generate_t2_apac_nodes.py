#!/usr/bin/env python3
"""
SRv6TEK Innovations - Tier-2-APAC Node Schema Generator
Automates Containerlab node mappings using Telstra AS4608.
"""

def build_apac_nodes(layout_strategy="vendor-mix"):
    # Authoritative Asia-Pacific Data Center Database
    pop_geo = {
        1: "tokyo_otemachi", 2: "osaka_telehouse", 3: "singapore_taiseng", 4: "hk_megai",
        5: "sydney_equinix", 6: "melbourne_nextdc", 7: "perth_nextdc", 8: "mumbai_gpx",
        9: "chennai_ntt", 10: "bangalore_stt", 11: "seoul_kinx", 12: "taipei_chief",
        13: "manila_vitro", 14: "jakarta_cyber", 15: "kl_aims", 16: "bangkok_telehouse",
        17: "hcmc_vnpt", 18: "auckland_datacom", 19: "guam_piti", 20: "honolulu_drfortress",
        21: "navi_mumbai_ctrls", 22: "delhi_webwerks", 23: "shima_landing"
    }
    
    asn = "4608"
    yaml_out = ["# ==============================================================================",
                f"# PROGRAMMATIC NODE MATRIX FOR TIER-2-APAC | CARRIER: TELSTRA (AS{asn})",
                "# ==============================================================================\n  nodes:"]

    for r in range(1, 135):
        node_id = f"R{r}"
        pop_idx = ((r - 1) // 4) + 1 if r <= 92 else 1
        pop_name = pop_geo.get(pop_idx, "backbone_cushion")

        if layout_strategy == "all-cisco":
            kind = "cisco_xrd"
        elif layout_strategy == "all-juniper":
            kind = "juniper_crpd"
        else:
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
    print(f"🟢 Generated Tier-2-APAC nodes.yaml using layout: {layout_strategy}")

if __name__ == "__main__":
    build_apac_nodes(layout_strategy="vendor-mix")
