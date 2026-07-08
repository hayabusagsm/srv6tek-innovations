#!/usr/bin/env python3
"""
SRv6TEK Innovations - Internet Simulation Programmatic Link Graph Builder
Calculates and wires explicitly numbered multi-tier interface interconnections.
"""

def generate_internet_sim_topology():
    clab_links = [
        "# ==============================================================================",
        "# INTERNET-SIM LINK FABRIC GRAPH DEFINITIONS (NUMBERED TRANSIT LAYER)",
        "# ==============================================================================\nlinks:"
    ]

    # Track sequential interface port assignments per node to guarantee zero structural drift
    port_tracker = {f"R{i}": 1 for i in range(1, 135)}
    for t in range(1, 5): port_tracker[f"TREX_0{t}"] = 1

    # Unique, structured inter-tier connectivity array
    interconnects = [
        # --- TIER-0 to TIER-1 TRANSIT CROSS-CONNECTS ---
        ("R1", "R5"), ("R1", "R6"),   # Amazon -> Verizon, AT&T
        ("R2", "R6"), ("R2", "R7"),   # Microsoft -> AT&T, TATA
        ("R3", "R7"), ("R3", "R8"),   # Google -> TATA, Deutsche Telekom
        ("R4", "R8"), ("R4", "R9"),   # Meta -> Deutsche Telekom, NTT
        
        # --- TIER-1 HORIZONTAL TRANSIT INTER-PEERING HIGHWAYS ---
        ("R5", "R6"), ("R6", "R7"), ("R7", "R8"), ("R8", "R9"),
        
        # --- TIER-1 Core Core Transit Down to TIER-2 Providers ---
        ("R5", "R46"), ("R6", "R52"), ("R7", "R58"), ("R8", "R64"), ("R9", "R70"),
        
        # --- TIER-2 REGIONAL INTER-PEERING MESH ---
        ("R46", "R52"), ("R52", "R58"), ("R58", "R64"), ("R64", "R70"), ("R70", "R76"), ("R76", "R82"),
        
        # --- TIER-2 down to TIER-3/CE Access Nodes ---
        ("R46", "R88"), ("R52", "R90"), ("R58", "R92"), ("R64", "R94"), ("R70", "R96"),
        
        # --- IXP / CDN INTERACTION STRATA ---
        ("R46", "R116"), ("R52", "R118"), ("R58", "R120"), ("R64", "R122"),
        ("R116", "R124"), ("R118", "R126"), ("R120", "R127"), ("R122", "R125")
    ]

    # Subnet seed parameters for numbered configurations
    v4_subnet_idx = 1
    v6_subnet_idx = 1

    clab_links.append("  # --- SECTION 1: CORE TRANSIT INTER-CONNECTIONS ---")
    for n1, n2 in interconnects:
        p1 = port_tracker[n1]
        p2 = port_tracker[n2]
        
        # Algorithmically calculate explicit IP configurations for verification
        v4_addr1 = f"10.200.{v4_subnet_idx}.1/30"
        v4_addr2 = f"10.200.{v4_subnet_idx}.2/30"
        v6_addr1 = f"2001:db8:ffff:{hex(v6_subnet_idx)[2:]}::1/64"
        v6_addr2 = f"2001:db8:ffff:{hex(v6_subnet_idx)[2:]}::2/64"

        clab_links.append(f"  - endpoints: [\"{n1}:eth{p1}\", \"{n2}:eth{p2}\"]")
        clab_links.append(f"    vars:")
        clab_links.append(f"      {n1}_ipv4: \"{v4_addr1}\"")
        clab_links.append(f"      {n2}_ipv4: \"{v4_addr2}\"")
        clab_links.append(f"      {n1}_ipv6: \"{v6_addr1}\"")
        clab_links.append(f"      {n2}_ipv6: \"{v6_addr2}\"")

        port_tracker[n1] += 1
        port_tracker[n2] += 1
        v4_subnet_idx += 1
        v6_subnet_idx += 1

    # Wire up the TRex traffic generation engines explicitly
    clab_links.append("\n  # --- SECTION 2: HIGH-VOLUME TRAFFIC INJECTOR LOOPS ---")
    trex_mappings = [("TREX_01", "R1"), ("TREX_02", "R2"), ("TREX_03", "R5"), ("TREX_04", "R9")]
    for trex, router in trex_mappings:
        tp = port_tracker[trex]
        rp = port_tracker[router]
        clab_links.append(f"  - endpoints: [\"{trex}:eth{tp}\", \"{router}:eth{rp}\"]")
        port_tracker[trex] += 1
        port_tracker[router] += 1

    with open("topology.yaml", "w") as f:
        f.write("\n".join(clab_links) + "\n")
    print("🟢 Internet Simulation topology.yaml link fabric generated successfully.")

if __name__ == "__main__":
    generate_internet_sim_topology()
