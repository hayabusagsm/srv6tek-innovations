#!/usr/bin/env python3
"""
SRv6TEK Innovations - Mega-Internet Topo Graph Builder
Algorithmically compiles the full custom 23-POP P2P graph for Containerlab.
Saves the completed network links definitions mapping straight into local topology.yaml.
"""

def generate_mega_internet_topology():
    clab_links = []
    clab_links.append("# ==============================================================================")
    clab_links.append("# CONSOLIDATED MEGA-INTERNET DIGITAL TWIN: SEAMLESS VENDOR-AGNOSTIC P2P LINKS")
    clab_links.append("# ==============================================================================\nlinks:")

    # 1. INTRA-POP DIRECT FABRIC TRUNKS (23 POPs x 1 link = 23 Links)
    # Direct 1-to-1 P <-> PE intra-chassis cross connect per data center facility.
    clab_links.append("  # --- INTRA-POP INTER-CHASSIS FABRIC LINKS (P <-> PE) ---")
    for pop in range(1, 24):
        node_p = f"R{2 * pop - 1}"
        node_pe = f"R{2 * pop}"
        clab_links.append(f"  - endpoints: [\"{node_p}:eth1\", \"{node_pe}:eth1\"]")

    # 2. LONG-HAUL SEGMENT CONNECTIONS & SUBSEA INTERCONNECTS
    clab_links.append("\n  # --- GLOBAL INTER-SEGMENT BACKBONE TRANSIT TRUNKS ---")
    
    # Space Segment: Starlink Orbital Tracks (R1 - R6)
    clab_links.append("  # Starlink Free-Space Optic (FSO) Laser Cross-Links")
    clab_links.append(f"  - endpoints: [\"R1:eth2\", \"R3:eth2\"]")
    clab_links.append(f"  - endpoints: [\"R3:eth3\", \"R5:eth2\"]")
    
    # Space-to-Ground: Laser Feeders down to Earth Ground Hubs
    clab_links.append("  # Starlink Laser Feeders down to Earth Ground Hubs")
    clab_links.append(f"  - endpoints: [\"R2:eth2\", \"R8:eth2\"]")   # Starlink down to Tier-1 USA (Ashburn)
    clab_links.append(f"  - endpoints: [\"R4:eth2\", \"R12:eth2\"]")  # Starlink down to Tier-1 EMEA (London)
    
    # Terrestrial Tier-1 Core Cross-AS Trunks (R7 - R20)
    clab_links.append("  # Tier-1 Transoceanic Subsea Pathways")
    clab_links.append(f"  - endpoints: [\"R7:eth2\", \"R11:eth2\"]")  # AS701 Ashburn <-> AS702 London (Transatlantic)
    clab_links.append(f"  - endpoints: [\"R9:eth2\", \"R15:eth2\"]")  # AS701 LA <-> AS703 Tokyo (Transpacific)
    clab_links.append(f"  - endpoints: [\"R11:eth3\", \"R15:eth3\"]") # AS702 London <-> AS703 Tokyo (Eurasian Highway)

    # Tier-2 Regional Eyeball Interconnects to Tier-1 Transit Core
    clab_links.append("  # Tier-2 High-Density Peering Handoffs to Tier-1 Transit Core")
    clab_links.append(f"  - endpoints: [\"R21:eth2\", \"R7:eth3\"]")  # Comcast USA <-> AS701 Core (Ashburn)
    clab_links.append(f"  - endpoints: [\"R31:eth2\", \"R11:eth4\"]") # Deutsche Telekom <-> AS702 Core (London)
    clab_links.append(f"  - endpoints: [\"R39:eth2\", \"R15:eth4\"]") # Telstra APAC <-> AS703 Core (Tokyo)

    # Cross-Tier-2 Horizontal Inter-Peering
    clab_links.append("  # Strategic Direct Settlement-Free Peering between Tier-2 Networks")
    clab_links.append(f"  - endpoints: [\"R23:eth2\", \"R33:eth2\"]") # Comcast NY <-> Deutsche Telekom Frankfurt (Private NNI)

    # Output directly as the clean local Containerlab link layout definition
    with open("topology.yaml", "w") as f:
        f.write("\n".join(clab_links) + "\n")
    print("🟢 Mega-Internet topology.yaml link definitions compiled natively inside local path context.")

if __name__ == "__main__":
    generate_mega_internet_topology()
