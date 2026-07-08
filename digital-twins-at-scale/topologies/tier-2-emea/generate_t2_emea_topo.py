#!/usr/bin/env python3
"""
SRv6TEK Innovations - Tier-2-EMEA Programmatic Topo Generator
Calculates dense European core rings + Mediterranean/African subsea landing spans.
"""

def build_emea_topology():
    clab_links = []
    clab_links.append("# ==============================================================================")
    clab_links.append("# PROGRAMMATIC TIER-2-EMEA DIGITAL TWIN: CONTAINERLAB P2P MESH MANIFEST")
    clab_links.append("# ==============================================================================\nlinks:")

    port_tracker = {f"R{i}": 1 for i in range(1, 135)}

    # 1. INTRA-POP FULL-MESH HA FABRICS
    clab_links.append("  # --- SECTION 1: INTRA-HOTEL FULL-MESH HA FABRICS ---")
    for pop in range(1, 24):
        p1, p2, pe1, pe2 = f"R{4*pop-3}", f"R{4*pop-2}", f"R{4*pop-1}", f"R{4*pop}"
        for n1, n2 in [(p1, p2), (p1, pe1), (p1, pe2), (p2, pe1), (p2, pe2)]:
            clab_links.append(f"  - endpoints: [\"{n1}:eth{port_tracker[n1]}\", \"{n2}:eth{port_tracker[n2]}\"]")
            port_tracker[n1] += 1; port_tracker[n2] += 1

    # 2. PROGRAMMATIC INTER-CITY EUROPEAN RING + PAN-AFRICAN LEAP
    clab_links.append("\n  # --- SECTION 2: FLAP RING + MEDITERRANEAN SUBSEA TRUNKS ---")
    # Programmatic FLAP Core Mesh: Interlinking London, Slough, Frankfurt, Amsterdam, Paris (POPs 1 to 5)
    for pop in range(1, 5):
        curr_p1, next_p1 = f"R{4*pop-3}", f"R{4*(pop+1)-3}"
        clab_links.append(f"  - endpoints: [\"{curr_p1}:eth{port_tracker[curr_p1]}\", \"{next_p1}:eth{port_tracker[next_p1]}\"]")
        port_tracker[curr_p1] += 1; port_tracker[next_p1] += 1
    # Close the FLAP core loop back from Paris (POP 5/R17) to London (POP 1/R1)
    clab_links.append(f"  - endpoints: [\"R17:eth{port_tracker['R17']}\", \"R1:eth{port_tracker['R1']}\"]")
    port_tracker['R17'] += 1; port_tracker['R1'] += 1

    # Marseille/Palermo/Madrid Mediterranean Pipeline (POPs 6 to 12 step loop)
    for pop in range(6, 12):
        curr_p1, next_p1 = f"R{4*pop-3}", f"R{4*(pop+1)-3}"
        clab_links.append(f"  - endpoints: [\"{curr_p1}:eth{port_tracker[curr_p1]}\", \"{next_p1}:eth{port_tracker[next_p1]}\"]")
        port_tracker[curr_p1] += 1; port_tracker[next_p1] += 1

    # Pan-African Subsea Trunk Algorithm: Connects Marseille (POP 6/R21) down to Cape Town (POP 22/R85)
    clab_links.append(f"  - endpoints: [\"R21:eth{port_tracker['R21']}\", \"R85:eth{port_tracker['R85']}\"]")
    port_tracker['R21'] += 1; port_tracker['R85'] += 1
    # Connect Cape Town (POP 22/R85) to Johannesburg (POP 23/R89)
    clab_links.append(f"  - endpoints: [\"R85:eth{port_tracker['R85']}\", \"R89:eth{port_tracker['R89']}\"]")
    port_tracker['R85'] += 1; port_tracker['R89'] += 1

    # 3. CONTROL PLANE & ACCESS EDGES INJECTION
    clab_links.append("\n  # --- SECTION 3: OUT-OF-PATH ROUTE REFLECTORS (R95 - R107) ---")
    for rr in range(95, 108):
        target_p = f"R{((rr - 95) % 5) * 4 + 1}"  # Bound tightly to primary FLAP core P1 nodes for stability
        clab_links.append(f"  - endpoints: [\"{target_p}:eth{port_tracker[target_p]}\", \"{rr}:eth{port_tracker[rr]}\"]")
        port_tracker[target_p] += 1; port_tracker[rr] += 1

    clab_links.append("\n  # --- SECTION 4: ENTERPRISE CUSTOMER EDGES (R108 - R130) ---")
    for ce in range(108, 131):
        target_pe = f"R{4*(ce-107)-1}"
        clab_links.append(f"  - endpoints: [\"{target_pe}:eth{port_tracker[target_pe]}\", \"{ce}:eth{port_tracker[ce]}\"]")
        port_tracker[target_pe] += 1; port_tracker[ce] += 1

    with open("topology.yaml", "w") as f:
        f.write("\n".join(clab_links) + "\n")
    print("🟢 Generated Tier-2-EMEA topology.yaml successfully.")

if __name__ == "__main__":
    build_emea_topology()
