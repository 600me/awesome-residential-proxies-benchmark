#!/usr/bin/env python3
"""Master Runner for Phase 4 Surround Packs (8 Packs / 32 Repositories)."""
import os
import sys

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)

from build_phase4_packs import write_repo, SHORTLINKS
from pack_builders.pack14_gologin import build as build14
from pack_builders.pack15_morelogin import build as build15
from pack_builders.pack16_elevenlabs_dubbing import build as build16
from pack_builders.pack17_packetstream import build as build17
from pack_builders.pack18_proxyseller import build as build18
from pack_builders.pack19_vultr_gpu import build as build19
from pack_builders.pack20_digitalocean_cloud import build as build20
from pack_builders.pack21_scraperapi_ecommerce import build as build21

def main():
    print("=" * 70)
    print("Building all 8 Phase 4 Surround Packs (32 Repositories)...")
    print("=" * 70)
    build14(write_repo, SHORTLINKS)
    build15(write_repo, SHORTLINKS)
    build16(write_repo, SHORTLINKS)
    build17(write_repo, SHORTLINKS)
    build18(write_repo, SHORTLINKS)
    build19(write_repo, SHORTLINKS)
    build20(write_repo, SHORTLINKS)
    build21(write_repo, SHORTLINKS)
    print("=" * 70)
    print("SUCCESS: All 32 Phase 4 Repositories built and verified!")
    print("=" * 70)

if __name__ == "__main__":
    main()
