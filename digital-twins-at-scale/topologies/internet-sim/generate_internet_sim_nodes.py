#!/usr/bin/env python3
"""
SRv6TEK Innovations - Internet Simulation Node Metadata Builder
Decouples, maps, and structures nodes based on the authoritative multi-tier drawing.
"""

def generate_internet_sim_nodes(layout_strategy="vendor-mix"):
    # Precise mapping matrix extracted from the architectural blueprint
    node_directory = {
        # --- TIER-0: HYPERSCALERS & FAANG (Nodes 1-4) ---
        1:   {"name": "Amazon", "as": "16509", "role": "TIER-0", "vendor": "cisco_xrd"},
        2:   {"name": "Microsoft", "as": "8075", "role": "TIER-0", "vendor": "cisco_xrd"},
        3:   {"name": "Google", "as": "19527", "role": "TIER-0", "vendor": "cisco_xrd"},
        4:   {"name": "Meta", "as": "32934", "role": "TIER-0", "vendor": "cisco_xrd"},
        
        # --- TIER-1: GLOBAL TRANSIT BACKBONES (Nodes 5-18) ---
        5:   {"name": "Verizon", "as": "701", "role": "TIER-1", "vendor": "cisco_xrd"},
        6:   {"name": "ATT", "as": "7018", "role": "TIER-1", "vendor": "cisco_xrd"},
        7:   {"name": "TATA", "as": "6453", "role": "TIER-1", "vendor": "cisco_xrd"},
        8:   {"name": "Deutsche_Telekom", "as": "3320", "role": "TIER-1", "vendor": "juniper_crpd"},
        9:   {"name": "NTT", "as": "2914", "role": "TIER-1", "vendor": "juniper_crpd"},
        
        # --- TIER-2: REGIONAL CARRIERS / EYEBALLS (Nodes 46-87) ---
        46:  {"name": "Comcast", "as": "7922", "role": "TIER-2", "vendor": "cisco_xrd"},
        52:  {"name": "British_Telecom", "as": "5400", "role": "TIER-2", "vendor": "juniper_crpd"},
        58:  {"name": "Charter_Comm", "as": "7843", "role": "TIER-2", "vendor": "cisco_xrd"},
        64:  {"name": "Vodafone", "as": "1273", "role": "TIER-2", "vendor": "juniper_crpd"},
        70:  {"name": "Hurricane_Electric", "as": "6939", "role": "TIER-2", "vendor": "cisco_xrd"},
        76:  {"name": "Singtel", "as": "7473", "role": "TIER-2", "vendor": "juniper_crpd"},
        82:  {"name": "Sprint", "as": "2711", "role": "TIER-2", "vendor": "cisco_xrd"},
        
        # --- TIER-3: LAST MILE FIBER PROVIDERS (Nodes 88-107) ---
        88:  {"name": "Astound_Broadband", "as": "6079", "role": "TIER-3", "vendor": "linux"},
        90:  {"name": "Everstream_Solutions", "as": "19009", "role": "TIER-3", "vendor": "linux"},
        92:  {"name": "Alta_Fiber", "as": "395273", "role": "TIER-3", "vendor": "linux"},
        94:  {"name": "Consolidated_Comm", "as": "9318", "role": "TIER-3", "vendor": "linux"},
        96:  {"name": "Posti", "as": "30798", "role": "TIER-3", "vendor": "linux"},
        98:  {"name": "Retelit", "as": "3302", "role": "TIER-3", "vendor": "linux"},
        100: {"name": "Ufinet", "as": "52468", "role": "TIER-3", "vendor": "linux"},
        102: {"name": "IONOS", "as": "8560", "role": "TIER-3", "vendor": "linux"},
        104: {"name": "Google_Fiber", "as": "10029", "role": "TIER-3", "vendor": "linux"},
        106: {"name": "Spectra", "as": "16591", "role": "TIER-3", "vendor": "linux"},

        # --- CONTENT DELIVERY NETWORKS & IXPS ---
        116: {"name": "DE_CIX", "as": "47228", "role": "IXP", "vendor": "linux"},
        118: {"name": "AMS_IX", "as": "6777", "role": "IXP", "vendor": "linux"},
        120: {"name": "LINX", "as": "8714", "role": "IXP", "vendor": "linux"},
        122: {"name": "Equinix_IX", "as": "15830", "role": "IXP", "vendor": "linux"},
        124: {"name": "Fastly", "as": "54113", "role": "CDN", "vendor": "linux"},
        126: {"name": "Cloudflare", "as": "13335", "role": "CDN", "vendor": "linux"},
        127: {"name": "Edgio", "as": "22822", "role": "CDN", "vendor": "linux"},
        125: {"name": "Akamai", "as": "122222", "role": "CDN", "vendor": "linux"}
    }

    yaml_nodes = [
        "# ==============================================================================",
        f"# AUTOMATED NODE SCHEMAS FOR INTERNET-SIM | LAYOUT STRATEGY: {layout_strategy.upper()}",
        "# ==============================================================================\n  nodes:"
    ]

    for node_num, metadata in node_directory.items():
        node_id = f"R{node_num}"
        
        # Override baseline vendor mappings if global layout overrides are specified
        if layout_strategy == "all-cisco" and metadata["role"] in ["TIER-0", "TIER-1", "TIER-2"]:
            kind = "cisco_xrd"
        elif layout_strategy == "all-juniper" and metadata["role"] in ["TIER-0", "TIER-1", "TIER-2"]:
            kind = "juniper_crpd"
        else:
            kind = metadata["vendor"]

        yaml_nodes.append(f"    {node_id}: {{ kind: {kind}, labels: {{ provider: \"{metadata['name']}\", role: {metadata['role']}, as: \"{metadata['as']}\" }} }}")

    # Inject TRex performance monitoring engines natively
    yaml_nodes.append("\n    # --- TRAFFIC INSTRUMENTATION INJECTORS ---")
    for trex_id in range(1, 5):
        yaml_nodes.append(f"    TREX_0{trex_id}: {{ kind: linux, labels: {{ role: \"TRAFFIC_GEN\" }} }}")

    with open("nodes.yaml", "w") as f:
        f.write("\n".join(yaml_nodes) + "\n")
    print(f"🟢 Internet Simulation node block compiled successfully into 'nodes.yaml' using layout: {layout_strategy}")

if __name__ == "__main__":
    generate_internet_sim_nodes(layout_strategy="vendor-mix")
