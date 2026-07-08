#!/usr/bin/env python3
"""
SRv6TEK Innovations - Algorithmic Containerlab Nodes Schema Generator
Appends matching device configurations tailored to specific vendor deployment strategies.
Outputs directly into 'nodes.yaml'.
"""

def generate_clab_nodes(topo_name="tier-1", layout_strategy="vendor-mix"):
    as_map = {
        "tier-1": "701", "tier-2-usa": "11427", "tier-2-emea": "3320", 
        "tier-2-apac": "4608", "starlink-space-ground": "701", "internet-sim": "701"
    }
    base_asn = as_map.get(topo_name, "1111")
    
    yaml_nodes = []
    yaml_nodes.append("# ==============================================================================")
    yaml_nodes.append(f"# AUTOMATED NODE SCHEMAS FOR TOPO: {topo_name.upper()} | LAYOUT: {layout_strategy.upper()}")
    yaml_nodes.append("# ==============================================================================\n  nodes:")

    for r in range(1, 135):
        node_id = f"R{r}"
        pop_idx = ((r - 1) // 4) + 1 if r <= 92 else 1
        
        if layout_strategy == "all-cisco":
            kind = "cisco_xrd"
        elif layout_strategy == "all-juniper":
            kind = "juniper_crpd"
        else:
            kind = "cisco_xrd" if pop_idx <= 12 or r > 92 else "juniper_crpd"

        if 1 <= r <= 94:
            role = "P" if (r - 1) % 4 < 2 else "PE"
            node_asn = base_asn
        elif 95 <= r <= 107:
            role = "RR"
            node_asn = base_asn
        else:
            role = "CE"
            node_asn = f"65{str(r).zfill(3)}"

        yaml_line = f"    {node_id}: {{ kind: {kind}, labels: {{ role: {role}, as: \"{node_asn}\" }} }}"
        yaml_nodes.append(yaml_line)

    with open("nodes.yaml", "w") as f:
        f.write("\n".join(yaml_nodes) + "\n")
    print(f"🟢 Nodes block generated successfully into 'nodes.yaml' for strategy: {layout_strategy}")

if __name__ == "__main__":
    generate_clab_nodes(topo_name="tier-1", layout_strategy="vendor-mix")
