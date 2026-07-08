#!/usr/bin/env python3
"""
SRv6TEK Innovations - Next-Gen Matrix Compiler
Outputs configurations natively inside localized topology subdirectories.
Permutations: 6 Topologies x 4 Technologies x 3 Vendor Layouts
"""

import os
from jinja2 import Environment, FileSystemLoader

TOPOLOGIES = ["internet-sim", "tier-1", "tier-2-usa", "tier-2-emea", "tier-2-apac", "starlink-space-ground", "mega-internet"]
TECHNOLOGIES = ["srv6", "mpls-ldp", "rsvp-te", "sr-mpls"]
VENDOR_LAYOUTS = ["all-cisco", "all-juniper", "vendor-mix"]

# Real-world Aggregate Networks and BGP Community Strings mapping
AS_DATABASE = {
    "701":   {"v4_agg": "192.0.2.0/24", "v6_agg": "2001:db8:701::/48", "primary_comm": "701:1000", "backup_comm": "701:2000"},
    "702":   {"v4_agg": "198.51.100.0/24", "v6_agg": "2001:db8:702::/48", "primary_comm": "702:1000", "backup_comm": "702:2000"},
    "703":   {"v4_agg": "203.0.113.0/24", "v6_agg": "2001:db8:703::/48", "primary_comm": "703:1000", "backup_comm": "703:2000"},
    "11427": {"v4_agg": "73.0.0.0/8", "v6_agg": "2001:558::/32", "primary_comm": "11427:1000", "backup_comm": "11427:2000"},
    "3320":  {"v4_agg": "80.0.0.0/8", "v6_agg": "2003::/19", "primary_comm": "3320:1000", "backup_comm": "3320:2000"},
    "4608":  {"v4_agg": "101.0.0.0/8", "v6_agg": "2001:4400::/32", "primary_comm": "4608:1000", "backup_comm": "4608:2000"}
}

def get_node_metadata(topo, tech, vendor_layout, node_num):
    node_id = f"R{node_num}"
    hex_id = f"{node_num:x}"
    pop_idx = ((node_num - 1) // 4) + 1 if node_num <= 92 else 1

    # Define Autonomous Systems based on Topology
    if topo in ["mega-internet", "internet-sim"]:
        if 1 <= node_num <= 6: asn = "701"
        elif 7 <= node_num <= 20: asn = "701" if node_num <= 10 else "702" if node_num <= 16 else "703"
        elif 21 <= node_num <= 30: asn = "11427"
        elif 31 <= node_num <= 38: asn = "3320"
        elif 39 <= node_num <= 46: asn = "4608"
        else: asn = "701"
    else:
        if topo == "tier-1": asn = "701" if node_num <= 46 else "702" if node_num <= 70 else "703"
        elif topo == "tier-2-usa": asn = "11427"
        elif topo == "tier-2-emea": asn = "3320"
        elif topo == "tier-2-apac": asn = "4608"
        else: asn = "701"

    # Hardware Platform Logic
    if vendor_layout == "all-cisco":
        kind = "cisco_xrd"
    elif vendor_layout == "all-juniper":
        kind = "juniper_crpd"
    else:
        kind = "cisco_xrd" if pop_idx <= 12 or node_num > 92 else "juniper_crpd"

    if 1 <= node_num <= 94:
        role = "P" if (node_num - 1) % 4 < 2 else "PE"
    elif 95 <= node_num <= 107:
        role = "RR"
    else:
        role = "CE"

    as_info = AS_DATABASE.get(asn, AS_DATABASE["701"])

    return {
        "node_id": node_id, "node_num": node_num, "kind": kind, "role": role, "asn": asn,
        "tech": tech, "loopback0": f"fc00:0:{hex_id}::1", "nsap": f"49.{asn.zfill(4)}.0000.0000.{str(node_num).zfill(4)}.00",
        "label_index": 1000 + node_num, "as_info": as_info, "routinator_ip": "192.168.1.235",
        "locators": {"main": f"fc00:0:{hex_id}::/48", "red": f"fc00:128:{hex_id}::/48", "green": f"fc00:129:{hex_id}::/48", "blue": f"fc00:130:{hex_id}::/48"},
        "rr_peers": [f"fc00:0:{hex(rr)[2:]}::1" for rr in ( if asn == "701" else)],
        "interfaces": [{"name": "eth1", "desc": "HA Fabric Link", "delay": 500}, {"name": "eth4", "desc": "Long-Haul Core Backhaul", "delay": 12000}],
        "all_pes": [f"fc00:0:{hex(i)[2:]}::1" for i in range(1, 95) if i % 2 == 0 and i != node_num]
    }

def compile_matrix():
    env = Environment(loader=FileSystemLoader('.'))
    for layout in VENDOR_LAYOUTS:
        for tech in TECHNOLOGIES:
            for topo in TOPOLOGIES:
                # NEW ROUTING PATH: digital-twins-at-scale/topologies/<topo>/compiled-configs/<tech>/
                output_dir = f"../topologies/{topo}/compiled-configs/{tech}"
                os.makedirs(output_dir, exist_ok=True)
                
                for node_num in range(1, 135):
                    ctx = get_node_metadata(topo, tech, layout, node_num)
                    if ctx["role"] == "CE": continue
                    
                    template_file = 'templates/juniper_multi.j2' if ctx["kind"] == "juniper_crpd" else 'templates/cisco_multi.j2'
                    template = env.get_template(template_file)
                    
                    config_out = template.render(node=ctx)
                    ext = "conf" if ctx["kind"] == "juniper_crpd" else "cfg"
                    
                    # Prefix file name with vendor layout layout to prevent naming collision in shared folder
                    with open(f"{output_dir}/{layout}_{ctx['node_id']}_config.{ext}", "w") as f:
                        f.write(config_out)
    print("✨ SSoT Localized Matrix Compiled. Configuration files cleanly nested inside corresponding topology paths.")

if __name__ == "__main__":
    compile_matrix()
