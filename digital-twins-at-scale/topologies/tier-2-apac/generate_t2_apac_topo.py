#!/usr/bin/env python3
"""
SRv6TEK Innovations - Tier-2-APAC Programmatic Topo Generator
Orchestrates long-reach transpacific subsea links and East Asian ring steps.
"""

def build_apac_topology():
    clab_links = []
    clab_links.append("# ==============================================================================")
    clab_links.append("# PROGRAMMATIC TIER-2-APAC DIGITAL TWIN: CONTAINERLAB P2P MESH MANIFEST")
    clab_links.append("# ==============================================================================\nlinks:")

    port_tracker = {f"R{i}": 1 for i in range(1, 135)}

    # 1. INTRA-POP FULL-MESH HA FABRICS
    clab_links.append("  # --- SECTION 1: INTRA-HOTEL FULL-MESH HA FABRICS ---")
    for pop in range(1, 24):
        p1, p2, pe1, pe2 = f"R{4*pop-3}", f"R{4*pop-2}", f"R{4*pop-1}", f"R{4*pop}"
        for n1, n2 in [(p1, p2), (p1, pe1), (p1, pe2), (p2, pe1), (p2, pe2)]:
            clab_links.append(f"  - endpoints: [\"{n1}:eth{port_tracker[n1]}\", \"{n2}:eth{port_tracker[n2]}\"]")
            port_tracker[n1] += 1; port_tracker[n2] += 1

    # 2. LONG-REACH TRANSOCEANIC SUBSEA STEP ALGORITHMS
    clab_links.append("\n  # --- SECTION 2: GEOGRAPHICALLY DISTRIBUTED OCEANIC SUBSEA SPANS ---")
    # East Asian Core Ring Step: Tokyo - Osaka - Singapore - Hong Kong (POPs 1 to 4)
    for pop in range(1, 4):
        curr_p1, next_p1 = f"R{4*pop-3}", f"R{4*(pop+1)-3}"
        clab_links.append(f"  - endpoints: [\"{curr_p1}:eth{port_tracker[curr_p1]}\", \"{next_p1}:eth{port_tracker[next_p1]}\"]")
        port_tracker[curr_p1] += 1; port_tracker[next_p1] += 1
    # Complete East Asian Loop: Hong Kong (POP 4/R13) back to Tokyo (POP 1/R1)
    clab_links.append(f"  - endpoints: [\"R13:eth{port_tracker['R13']}\", \"R1:eth{port_tracker['R1']}\"]")
    port_tracker['R13'] += 1; port_tracker['R1'] += 1

    # Oceania South Pacific Backbone Ring: Chaining Sydney, Melbourne, Perth (POPs 5 to 7)
    for pop in range(5, 7):
        curr_p1, next_p1 = f"R{4*pop-3}", f"R{4*(pop+1)-3}"
        clab_links.append(f"  - endpoints: [\"{curr_p1}:eth{port_tracker[curr_p1]}\", \"{next_p1}:eth{port_tracker[next_p1]}\"]")
        port_tracker[curr_p1] += 1; port_tracker[next_p1] += 1
    # Core Subsea Link: Connect Singapore (POP 3/R9) straight to Perth (POP 7/R25) (Indigo Cable Model)
    clab_links.append(f"  - endpoints: [\"R9:eth{port_tracker['R9']}\", \"R25:eth{port_tracker['R25']}\"]")
    port_tracker['R9'] += 1; port_tracker['R25'] += 1

    # Pacific Island Hopping Gateway: Tokyo (POP 1/R1) -> Guam (POP 19/R73) -> Honolulu (POP 20/R77) -> Sydney (POP 5/R17)
    clab_links.append(f"  - endpoints: [\"R1:eth{port_tracker['R1']}\", \"R73:eth{port_tracker['R73']}\"]")
    clab_links.append(f"  - endpoints: [\"R73:eth{port_tracker['R73']}\", \"R77:eth{port_tracker['R77']}\"]")
    clab_links.append(f"  - endpoints: [\"R77:eth{port_tracker['R77']}\", \"R17:eth{port_tracker['R17']}\"]")
    port_tracker['R1'] += 1; port_tracker['R73'] += 2; port_tracker['R77'] += 2; port_tracker['R17'] += 1

    # 3. CONTROL PLANE & ACCESS EDGES INJECTION
    clab_links.append("\n  # --- SECTION 3: OUT-OF-PATH ROUTE REFLECTORS (R95 - R107) ---")
    for rr in range(95, 108):
        target_p = f"R{((rr - 95) % 4) * 4 + 1}"  # Distributed across the East Asian core switching nodes
        clab_links.append(f"  - endpoints: [\"{target_p}:eth{port_tracker[target_p]}\", \"{rr}:eth{port_tracker[rr]}\"]")
        port_tracker[target_p] += 1; port_tracker[rr] += 1

    clab_links.append("\n  # --- SECTION 4: ENTERPRISE CUSTOMER EDGES (R108 - R130) ---")
    for ce in range(108, 131):
        target_pe = f"R{4*(ce-107)-1}"
        clab_links.append(f"  - endpoints: [\"{target_pe}:eth{port_tracker[target_pe]}\", \"{ce}:eth{port_tracker[ce]}\"]")
        port_tracker[target_pe] += 1; port_tracker[ce] += 1

    with open("topology.yaml", "w") as f:
        f.write("\n".join(clab_links) + "\n")
    print("🟢 Generated Tier-2-APAC topology.yaml successfully.")

if __name__ == "__main__":
    build_apac_topology()
