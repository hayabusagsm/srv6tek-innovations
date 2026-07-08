#!/usr/bin/env python3
"""
SRv6TEK Innovations - Universal Turnkey Manifest Assembler
Glues local node and link topology fragments into production-ready Containerlab manifests.
Features automated folder context discovery to remain fully portable across directories.
"""

import os
import subprocess

# ==============================================================================
# 🛰️ UNIVERSAL DOCKER REGISTRY SETTINGS & PARAMETERS
# ==============================================================================
MGMT_NET = "mgt_net"
MGMT_V4_SUBNET = "172.20.20.0/24"
MGMT_V6_SUBNET = "2001:172:20:20::/80"

# Production Verified Container Paths
IMG_CISCO = "ios-xr/xrd-control-plane:25.2.2"
IMG_JUNIPER_EVO = "cjunosevolved:25.4r1.13-evo"
IMG_JUNIPER_CRPD = "crpd:25.4R1.12"

TECHNOLOGIES = ["srv6", "sr-mpls", "mpls-ldp", "rsvp-te"]
LAYOUTS = ["cisco", "juniper", "mix"]

def discover_topology_context():
    """Dynamically captures the active folder name to use as the topology name."""
    current_absolute_path = os.getcwd()
    folder_name = os.path.basename(current_absolute_path)
    return folder_name

def run_local_fragment_generators():
    """Runs your pre-built node and topology scripts to compute local link outputs."""
    print("⏳ Executing local algorithmic network calculators...")
    
    node_script = [f for f in os.listdir('.') if f.endswith('nodes.py')]
    topo_script = [f for f in os.listdir('.') if f.endswith('topo.py')]
    
    if node_script:
        print(f"  ↳ Running: {node_script[0]}")
        subprocess.run(["python3", node_script[0]], check=True)
    
    if topo_script:
        print(f"  ↳ Running: {topo_script[0]}")
        subprocess.run(["python3", topo_script[0]], check=True)

def parse_txt_fragment(filename):
    """Parses text file fragments cleanly into memory arrays."""
    lines = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                lines.append(line.rstrip())
    return lines

def assemble_manifest_matrix():
    # 1. Dynamically capture the active topology context
    topo_name = discover_topology_context()
    
    # 2. Re-compute local infrastructure mapping variables
    run_local_fragment_generators()
    
    # 3. Read the calculated nodes and link fragments
    raw_nodes = parse_txt_fragment("nodes.yaml")
    raw_links = parse_txt_fragment("topology.yaml")
    
    print(f"🪡 Stitching [{topo_name}] manifests against Docker imaging variables...")
    
    for tech in TECHNOLOGIES:
        for layout in LAYOUTS:
            # 4. Formulate the Global Manifest Parameters Header block
            manifest = [
                f"# ==============================================================================",
                f"# SRv6TEK Innovations - Final Unified Production Topology Manifest",
                f"# Topology: {topo_name.upper()} | Technology: {tech.upper()} | Profile: {layout.upper()}",
                f"# ==============================================================================",
                f"name: srv6tek-{topo_name}-{layout}-{tech}",
                f"mgmt:",
                f"  network: {MGMT_NET}",
                f"  ipv4-subnet: {MGMT_V4_SUBNET}",
                f"  ipv6-subnet: {MGMT_V6_SUBNET}\n",
                f"topology:",
                f"  kinds:",
                f"    cisco_xrd:",
                f"      image: {IMG_CISCO}",
                f"      restart-policy: \"no\"",
                f"    juniper_cjunosevolved:",
                f"      image: {IMG_JUNIPER_EVO}",
                f"      restart-policy: \"no\"",
                f"    juniper_crpd:",
                f"      image: {IMG_JUNIPER_CRPD}",
                f"      restart-policy: \"no\"\n",
                f"  nodes:"
            ]
            
            # 5. Process and format every single node injection dynamically
            for line in raw_nodes:
                clean_line = line.strip()
                if not clean_line or clean_line.startswith("#") or "nodes:" in clean_line:
                    continue
                
                parts = clean_line.split(":")
                raw_node_id = parts[0].strip()
                node_id = raw_node_id.replace("{", "").replace("}", "").strip()
                
                try:
                    if node_id.startswith("R"):
                        node_num = int(node_id.replace("R", ""))
                    elif "TEX" in node_id or "TREX" in node_id:
                        node_num = 200 + int(node_id.split("_")[-1])
                    else:
                        node_num = 250
                except Exception:
                    node_num = 254

                m_v4 = f"172.20.20.{node_num}"
                m_v6 = f"2001:172:20:20::{node_num}"
                cfg_file = f"compiled-configs/{tech}/{layout}_{node_id}.cfg"
                
                # Determine precise hardware kind platform routing rules
                if layout == "cisco":
                    kind = "cisco_xrd"
                elif layout == "juniper":
                    if tech == "srv6" and node_id.startswith("R") and node_num <= 107:
                        kind = "juniper_cjunosevolved"
                    else:
                        kind = "juniper_crpd"
                else: # "mix" -> 50/50 hardware partition split rule
                    pop_idx = ((node_num - 1) // 4) + 1 if node_id.startswith("R") and node_num <= 92 else 1
                    if pop_idx <= 12 or node_num > 92 or not node_id.startswith("R"):
                        kind = "cisco_xrd"
                    else:
                        if tech == "srv6" and node_num <= 107:
                            kind = "juniper_cjunosevolved"
                        else:
                            kind = "juniper_crpd"

                manifest.append(f"    {node_id}:")
                manifest.append(f"      kind: {kind}")
                manifest.append(f"      mgmt-ipv4: {m_v4}")
                manifest.append(f"      mgmt-ipv6: {m_v6}")
                
                if not node_id.startswith("TEX") and not node_id.startswith("TREX"):
                    manifest.append(f"      startup-config: {cfg_file}")
                
            # 6. Append the physical P2P links definition map
            manifest.append("\n  links:")
            for line in raw_links:
                clean_link = line.strip()
                if not clean_link or "links:" in clean_link or clean_link.startswith("#"):
                    continue
                manifest.append(f"    {line}")
                
            # 7. Output the completed turnkey manifest directly to local directory
            output_filename = f"{layout}_{tech}.clab.yaml"
            with open(output_filename, "w") as mf:
                mf.write("\n".join(manifest) + "\n")
                
    # 8. Tidy up temporary output fragments
    for temp_file in ["nodes.yaml", "topology.yaml"]:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
    print(f"✨ Assembled Successfully! 12 production files generated for [{topo_name}].")

if __name__ == "__main__":
    assemble_manifest_matrix()
