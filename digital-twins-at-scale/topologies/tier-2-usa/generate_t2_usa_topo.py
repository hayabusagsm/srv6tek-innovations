#!/usr/bin/env python3
"""
SRv6TEK Innovations - Tier-2-USA Programmatic Topo Generator
Algorithmically builds a dual-ring cross-continental grid (23 POPs x 4 nodes).
"""

def build_usa_topology():
    clab_links = []
    clab_links.append("# ==============================================================================")
    clab_links.append("# PROGRAMMATIC TIER-2-USA DIGITAL TWIN: CONTAINERLAB P2P MESH MANIFEST")
    clab_links.append("# ==============================================================================\nlinks:")

    # Track sequential interfaces per node to avoid collisions (start at data port eth1)
    port_tracker = {f"R{i}": 1 for i in range(1, 135)}

    # 1. INTRA-POP FULL-MESH HA FABRICS (23 POPs x 5 links = 115 Links)
    clab_links.append("  # --- SECTION 1: INTRA-HOTEL FULL-MESH HA FABRICS ---")
    for pop in range(1, 24):
        p1, p2, pe1, pe2 = f"R{4*pop-3}", f"R{4*pop-2}", f"R{4*pop-1}", f"R{4*pop}"
        for n1, n2 in [(p1, p2), (p1, pe1), (p1, pe2), (p2, pe1), (p2, pe2)]:
            clab_links.append(f"  - endpoints: [\"{n1}:eth{port_tracker[n1]}\", \"{n2}:eth{port_tracker[n2]}\"]")
            port_tracker[n1] += 1; port_tracker[n2] += 1

    # 2. PROGRAMMATIC INTER-CITY TERRESTRIAL GRID TRACKS
    clab_links.append("\n  # --- SECTION 2: DYNAMIC INTER-CITY TERRESTRIAL TRUNKS ---")
    # East Coast Transit Belt: POPs 1 to 7 chained sequentially
    for pop in range(1, 7):
        curr_p1, next_p1 = f"R{4*pop-3}", f"R{4*(pop+1)-3}"
        clab_links.append(f"  - endpoints: [\"{curr_p1}:eth{port_tracker[curr_p1]}\", \"{next_p1}:eth{port_tracker[next_p1]}\"]")
        port_tracker[curr_p1] += 1; port_tracker[next_p1] += 1

    # Central Crossroads Grid: Chaining POPs 8 to 13, and cross-linking back to East Coast
    for pop in range(8, 13):
        curr_p1, next_p1 = f"R{4*pop-3}", f"R{4*(pop+1)-3}"
        clab_links.append(f"  - endpoints: [\"{curr_p1}:eth{port_tracker[curr_p1]}\", \"{next_p1}:eth{port_tracker[next_p1]}\"]")
        port_tracker[curr_p1] += 1; port_tracker[next_p1] += 1
    # Cross-connect Chicago (POP 8/R29) back to Ashburn (POP 1/R1) for central core stability
    clab_links.append(f"  - endpoints: [\"R29:eth{port_tracker['R29']}\", \"R1:eth{port_tracker['R1']}\"]")
    port_tracker['R29'] += 1; port_tracker['R1'] += 1

    # West Coast Gateway Belt: Chaining POPs 14 to 23
    for pop in range(14, 23):
        curr_p1, next_p1 = f"R{4*pop-3}", f"R{4*(pop+1)-3}"
        clab_links.append(f"  - endpoints: [\"{curr_p1}:eth{port_tracker[curr_p1]}\", \"{next_p1}:eth{port_tracker[next_p1]}\"]")
        port_tracker[curr_p1] += 1; port_tracker[next_p1] += 1

    # 3. CONTROL PLANE & ACCESS EDGES INJECTION
    clab_links.append("\n  # --- SECTION 3: OUT-OF-PATH ROUTE REFLECTORS (R95 - R107) ---")
    for rr in range(95, 108):
        target_p = f"R{((rr - 95) % 23) * 4 + 1}"  # Balanced distribution across P1 nodes
        clab_links.append(f"  - endpoints: [\"{target_p}:eth{port_tracker[target_p]}\", \"{rr}:eth{port_tracker[rr]}\"]")
        port_tracker[target_p] += 1; port_tracker[rr] += 1

    clab_links.append("\n  # --- SECTION 4: ENTERPRISE CUSTOMER EDGES (R108 - R130) ---")
    for ce in range(108, 131):
        target_pe = f"R{4*(ce-107)-1}"  # Single-homed to local PE1 routers sequentially
        clab_links.append(f"  - endpoints: [\"{target_pe}:eth{port_tracker[target_pe]}\", \"{ce}:eth{port_tracker[ce]}\"]")
        port_tracker[target_pe] += 1; port_tracker[ce] += 1

    with open("topology.yaml", "w") as f:
        f.write("\n".join(clab_links) + "\n")
    print("🟢 Generated Tier-2-USA topology.yaml successfully.")

if __name__ == "__main__":
    build_usa_topology()
