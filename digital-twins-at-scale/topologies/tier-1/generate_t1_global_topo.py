#!/usr/bin/env python3
"""
SRv6TEK Innovations - Tier-1 Global Core Programmatic Topo Generator
Calculates separate infrastructure loops for AS701, AS702, and AS703,
then mathematically injects the inter-AS transoceanic core boundaries.
"""

def build_t1_topology():
    clab_links = []
    clab_links.append("# ==============================================================================")
    clab_links.append("# PROGRAMMATIC TIER-1 MULTI-AS GLOBAL CORE: CONTAINERLAB P2P MESH MANIFEST")
    clab_links.append("# ==============================================================================\nlinks:")

    port_tracker = {f"R{i}": 1 for i in range(1, 135)}

    # 1. INTRA-POP FULL-MESH HA FABRICS
    clab_links.append("  # --- SECTION 1: INTRA-HOTEL FULL-MESH HA FABRICS ---")
    for pop in range(1, 24):
        p1, p2, pe1, pe2 = f"R{4*pop-3}", f"R{4*pop-2}", f"R{4*pop-1}", f"R{4*pop}"
        for n1, n2 in [(p1, p2), (p1, pe1), (p1, pe2), (p2, pe1), (p2, pe2)]:
            clab_links.append(f"  - endpoints: [\"{n1}:eth{port_tracker[n1]}\", \"{n2}:eth{port_tracker[n2]}\"]")
            port_tracker[n1] += 1; port_tracker[n2] += 1

    # 2. INTER-CITY TRUNKING SEGREGATED ALGORITHMICALLY BY AUTONOMOUS SYSTEM
    clab_links.append("\n  # --- SECTION 2: INTRA-AS BACKBONE REGIONAL PIPELINES ---")
    
    # 🇺🇸 AS701 North American Transit Core Loop (POPs 1 to 11 / Nodes R1 - R44)
    for pop in range(1, 11):
        curr_p1, next_p1 = f"R{4*pop-3}", f"R{4*(pop+1)-3}"
        clab_links.append(f"  - endpoints: [\"{curr_p1}:eth{port_tracker[curr_p1]}\", \"{next_p1}:eth{port_tracker[next_p1]}\"]")
        port_tracker[curr_p1] += 1; port_tracker[next_p1] += 1

    # 🇪🇺 AS702 Pan-European Transit Core Loop (POPs 12 to 17 / Nodes R45 - R68)
    for pop in range(12, 17):
        curr_p1, next_p1 = f"R{4*pop-3}", f"R{4*(pop+1)-3}"
        clab_links.append(f"  - endpoints: [\"{curr_p1}:eth{port_tracker[curr_p1]}\", \"{next_p1}:eth{port_tracker[next_p1]}\"]")
        port_tracker[curr_p1] += 1; port_tracker[next_p1] += 1

    # 🌏 AS703 Asia-Pacific Core Loop (POPs 18 to 23 / Nodes R69 - R92)
    for pop in range(18, 23):
        curr_p1, next_p1 = f"R{4*pop-3}", f"R{4*(pop+1)-3}"
        clab_links.append(f"  - endpoints: [\"{curr_p1}:eth{port_tracker[curr_p1]}\", \"{next_p1}:eth{port_tracker[next_p1]}\"]")
        port_tracker[curr_p1] += 1; port_tracker[next_p1] += 1

    # 🌊 THE SEAMLESS INTER-AS TRANSOCEANIC COUPLERS
    clab_links.append("\n  # --- SECTION 2B: AUTHORITATIVE INTER-AS TRANSOCEANIC CORE SPANS ---")
    # Transatlantic Subsea: New York (AS701 / POP 2 / R5) <-> London (AS702 / POP 12 / R45)
    clab_links.append(f"  - endpoints: [\"R5:eth{port_tracker['R5']}\", \"R45:eth{port_tracker['R45']}\"]")
    port_tracker['R5'] += 1; port_tracker['R45'] += 1

    # Transpacific Subsea: Los Angeles (AS701 / POP 11 / R41) <-> Tokyo (AS703 / POP 18 / R69)
    clab_links.append(f"  - endpoints: [\"R41:eth{port_tracker['R41']}\", \"R69:eth{port_tracker['R69']}\"]")
    port_tracker['R41'] += 1; port_tracker['R69'] += 1

    # 3. CONTROL PLANE & ACCESS EDGES INJECTION
    clab_links.append("\n  # --- SECTION 3: MULTI-AS OUT-OF-PATH ROUTE REFLECTORS (R95 - R107) ---")
    for rr in range(95, 108):
        # Dynamically matches the RR to its appropriate parent AS core infrastructure loop
        target_p = f"R{((rr - 95) % 23) * 4 + 1}"
        clab_links.append(f"  - endpoints: [\"{target_p}:eth{port_tracker[target_p]}\", \"{rr}:eth{port_tracker[rr]}\"]")
        port_tracker[target_p] += 1; port_tracker[rr] += 1

    clab_links.append("\n  # --- SECTION 4: DISTRIBUTED CUSTOMER ACCESS EDGES (R108 - R130) ---")
    for ce in range(108, 131):
        target_pe = f"R{4*(ce-107)-1}"
        clab_links.append(f"  - endpoints: [\"{target_pe}:eth{port_tracker[target_pe]}\", \"{ce}:eth{port_tracker[ce]}\"]")
        port_tracker[target_pe] += 1; port_tracker[ce] += 1

    with open("topology.yaml", "w") as f:
        f.write("\n".join(clab_links) + "\n")
    print("🟢 Generated Tier-1 Global Core topology.yaml successfully.")

if __name__ == "__main__":
    build_t1_topology()
