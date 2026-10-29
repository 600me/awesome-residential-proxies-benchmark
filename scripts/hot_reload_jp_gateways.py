#!/usr/bin/env python3
import subprocess
import sys

def main():
    print("[*] Fetching current /etc/nginx/sites-available/jp-cps-gateways from jp-server...")
    raw = subprocess.check_output(['ssh', 'jp-server', 'cat /etc/nginx/sites-available/jp-cps-gateways']).decode('utf-8')
    
    # 1. Update dusen.party: MoreLogin real link
    dusen_ml_old = """    # MoreLogin (/ml/1..4) - Multi-login Browser (fallback to AdsPower share link)
    location = /ml/1 { return 302 "https://app.adspower.net/registration?code=bGrcRR&utm_source=github&utm_campaign=morelogin_tco&utm_content=dusen_ml1"; }
    location = /ml/2 { return 302 "https://app.adspower.net/registration?code=bGrcRR&utm_source=github&utm_campaign=morelogin_tco&utm_content=dusen_ml2"; }
    location = /ml/3 { return 302 "https://app.adspower.net/registration?code=bGrcRR&utm_source=github&utm_campaign=morelogin_tco&utm_content=dusen_ml3"; }
    location = /ml/4 { return 302 "https://app.adspower.net/registration?code=bGrcRR&utm_source=github&utm_campaign=morelogin_tco&utm_content=dusen_ml4"; }"""

    dusen_ml_new = """    # MoreLogin (/ml/1..4) - Multi-login Browser (Verified Real Link)
    location = /ml/1 { return 302 "https://www.morelogin.com/?from=AAChzMeApyIn&utm_source=github&utm_campaign=morelogin_tco&utm_content=dusen_ml1"; }
    location = /ml/2 { return 302 "https://www.morelogin.com/?from=AAChzMeApyIn&utm_source=github&utm_campaign=morelogin_tco&utm_content=dusen_ml2"; }
    location = /ml/3 { return 302 "https://www.morelogin.com/?from=AAChzMeApyIn&utm_source=github&utm_campaign=morelogin_tco&utm_content=dusen_ml3"; }
    location = /ml/4 { return 302 "https://www.morelogin.com/?from=AAChzMeApyIn&utm_source=github&utm_campaign=morelogin_tco&utm_content=dusen_ml4"; }"""

    # Add HeyGen to dusen.party
    dusen_el2_old = """    # ElevenLabs Dubbing (/el2/1..4) - Enterprise Dubbing & Localization
    location = /el2/1 { return 302 "https://try.elevenlabs.io/lo3kb8cy0f6v?utm_source=github&utm_campaign=dubbing_tco&utm_content=dusen_el2_1"; }
    location = /el2/2 { return 302 "https://try.elevenlabs.io/lo3kb8cy0f6v?utm_source=github&utm_campaign=dubbing_tco&utm_content=dusen_el2_2"; }
    location = /el2/3 { return 302 "https://try.elevenlabs.io/lo3kb8cy0f6v?utm_source=github&utm_campaign=dubbing_tco&utm_content=dusen_el2_3"; }
    location = /el2/4 { return 302 "https://try.elevenlabs.io/lo3kb8cy0f6v?utm_source=github&utm_campaign=dubbing_tco&utm_content=dusen_el2_4"; }"""

    dusen_el2_and_hg_new = """    # ElevenLabs Dubbing (/el2/1..4) - Enterprise Dubbing & Localization
    location = /el2/1 { return 302 "https://try.elevenlabs.io/lo3kb8cy0f6v?utm_source=github&utm_campaign=dubbing_tco&utm_content=dusen_el2_1"; }
    location = /el2/2 { return 302 "https://try.elevenlabs.io/lo3kb8cy0f6v?utm_source=github&utm_campaign=dubbing_tco&utm_content=dusen_el2_2"; }
    location = /el2/3 { return 302 "https://try.elevenlabs.io/lo3kb8cy0f6v?utm_source=github&utm_campaign=dubbing_tco&utm_content=dusen_el2_3"; }
    location = /el2/4 { return 302 "https://try.elevenlabs.io/lo3kb8cy0f6v?utm_source=github&utm_campaign=dubbing_tco&utm_content=dusen_el2_4"; }

    # HeyGen (/hg/1..4) - AI Video & Digital Avatar (Verified Rewardful Real Link)
    location = /hg/1 { return 302 "https://www.heygen.com/?sid=rewardful&utm_content=creator&utm_medium=influencera&via=kais&utm_source=github&utm_campaign=heygen_tco&utm_content=dusen_hg1"; }
    location = /hg/2 { return 302 "https://www.heygen.com/?sid=rewardful&utm_content=creator&utm_medium=influencera&via=kais&utm_source=github&utm_campaign=heygen_tco&utm_content=dusen_hg2"; }
    location = /hg/3 { return 302 "https://www.heygen.com/?sid=rewardful&utm_content=creator&utm_medium=influencera&via=kais&utm_source=github&utm_campaign=heygen_tco&utm_content=dusen_hg3"; }
    location = /hg/4 { return 302 "https://www.heygen.com/?sid=rewardful&utm_content=creator&utm_medium=influencera&via=kais&utm_source=github&utm_campaign=heygen_tco&utm_content=dusen_hg4"; }"""

    # 2. Update norb.date: MoreLogin real link and PacketStream real link
    norb_ml_old = """    # MoreLogin (/ml/1..4) on norb
    location = /ml/1 { return 302 "https://app.adspower.net/registration?code=bGrcRR&utm_source=github&utm_campaign=morelogin_tco&utm_content=norb_ml1"; }
    location = /ml/2 { return 302 "https://app.adspower.net/registration?code=bGrcRR&utm_source=github&utm_campaign=morelogin_tco&utm_content=norb_ml2"; }
    location = /ml/3 { return 302 "https://app.adspower.net/registration?code=bGrcRR&utm_source=github&utm_campaign=morelogin_tco&utm_content=norb_ml3"; }
    location = /ml/4 { return 302 "https://app.adspower.net/registration?code=bGrcRR&utm_source=github&utm_campaign=morelogin_tco&utm_content=norb_ml4"; }"""

    norb_ml_new = """    # MoreLogin (/ml/1..4) on norb (Verified Real Link)
    location = /ml/1 { return 302 "https://www.morelogin.com/?from=AAChzMeApyIn&utm_source=github&utm_campaign=morelogin_tco&utm_content=norb_ml1"; }
    location = /ml/2 { return 302 "https://www.morelogin.com/?from=AAChzMeApyIn&utm_source=github&utm_campaign=morelogin_tco&utm_content=norb_ml2"; }
    location = /ml/3 { return 302 "https://www.morelogin.com/?from=AAChzMeApyIn&utm_source=github&utm_campaign=morelogin_tco&utm_content=norb_ml3"; }
    location = /ml/4 { return 302 "https://www.morelogin.com/?from=AAChzMeApyIn&utm_source=github&utm_campaign=morelogin_tco&utm_content=norb_ml4"; }"""

    norb_ps_old = """    # PacketStream (/ps/1..4) - Residential Proxy Pool (fallback to Pawns)
    location = /ps/1 { return 302 "https://pawns.app/?r=20796407&utm_source=github&utm_campaign=packetstream_tco&utm_content=norb_ps1"; }
    location = /ps/2 { return 302 "https://pawns.app/?r=20796407&utm_source=github&utm_campaign=packetstream_tco&utm_content=norb_ps2"; }
    location = /ps/3 { return 302 "https://pawns.app/?r=20796407&utm_source=github&utm_campaign=packetstream_tco&utm_content=norb_ps3"; }
    location = /ps/4 { return 302 "https://pawns.app/?r=20796407&utm_source=github&utm_campaign=packetstream_tco&utm_content=norb_ps4"; }"""

    norb_ps_new = """    # PacketStream (/ps/1..4) - Residential Proxy Pool (Verified Real Link)
    location = /ps/1 { return 302 "https://packetstream.io/?psr=n082d9gsbh&utm_source=github&utm_campaign=packetstream_tco&utm_content=norb_ps1"; }
    location = /ps/2 { return 302 "https://packetstream.io/?psr=n082d9gsbh&utm_source=github&utm_campaign=packetstream_tco&utm_content=norb_ps2"; }
    location = /ps/3 { return 302 "https://packetstream.io/?psr=n082d9gsbh&utm_source=github&utm_campaign=packetstream_tco&utm_content=norb_ps3"; }
    location = /ps/4 { return 302 "https://packetstream.io/?psr=n082d9gsbh&utm_source=github&utm_campaign=packetstream_tco&utm_content=norb_ps4"; }"""

    # 3. Update zelumo.top: PacketStream real link
    zelumo_ps_old = """    # PacketStream (/ps/1..4) on zelumo
    location = /ps/1 { return 302 "https://pawns.app/?r=20796407&utm_source=github&utm_campaign=packetstream_tco&utm_content=zelumo_ps1"; }
    location = /ps/2 { return 302 "https://pawns.app/?r=20796407&utm_source=github&utm_campaign=packetstream_tco&utm_content=zelumo_ps2"; }
    location = /ps/3 { return 302 "https://pawns.app/?r=20796407&utm_source=github&utm_campaign=packetstream_tco&utm_content=zelumo_ps3"; }
    location = /ps/4 { return 302 "https://pawns.app/?r=20796407&utm_source=github&utm_campaign=packetstream_tco&utm_content=zelumo_ps4"; }"""

    zelumo_ps_new = """    # PacketStream (/ps/1..4) on zelumo (Verified Real Link)
    location = /ps/1 { return 302 "https://packetstream.io/?psr=n082d9gsbh&utm_source=github&utm_campaign=packetstream_tco&utm_content=zelumo_ps1"; }
    location = /ps/2 { return 302 "https://packetstream.io/?psr=n082d9gsbh&utm_source=github&utm_campaign=packetstream_tco&utm_content=zelumo_ps2"; }
    location = /ps/3 { return 302 "https://packetstream.io/?psr=n082d9gsbh&utm_source=github&utm_campaign=packetstream_tco&utm_content=zelumo_ps3"; }
    location = /ps/4 { return 302 "https://packetstream.io/?psr=n082d9gsbh&utm_source=github&utm_campaign=packetstream_tco&utm_content=zelumo_ps4"; }"""

    new_cfg = raw
    assert dusen_ml_old in new_cfg, "dusen_ml_old block not found!"
    new_cfg = new_cfg.replace(dusen_ml_old, dusen_ml_new)

    assert dusen_el2_old in new_cfg, "dusen_el2_old block not found!"
    new_cfg = new_cfg.replace(dusen_el2_old, dusen_el2_and_hg_new)

    assert norb_ml_old in new_cfg, "norb_ml_old block not found!"
    new_cfg = new_cfg.replace(norb_ml_old, norb_ml_new)

    assert norb_ps_old in new_cfg, "norb_ps_old block not found!"
    new_cfg = new_cfg.replace(norb_ps_old, norb_ps_new)

    assert zelumo_ps_old in new_cfg, "zelumo_ps_old block not found!"
    new_cfg = new_cfg.replace(zelumo_ps_old, zelumo_ps_new)

    print("[*] Successfully replaced all gateway blocks. Writing back to jp-server...")
    proc = subprocess.Popen(['ssh', 'jp-server', 'cat > /etc/nginx/sites-available/jp-cps-gateways'], stdin=subprocess.PIPE)
    proc.communicate(input=new_cfg.encode('utf-8'))
    if proc.returncode != 0:
        print("[!] Error writing to jp-server!")
        sys.exit(1)

    print("[*] Testing nginx configuration on jp-server...")
    res_t = subprocess.run(['ssh', 'jp-server', 'nginx -t'], capture_output=True, text=True)
    print(res_t.stderr or res_t.stdout)
    if res_t.returncode != 0:
        print("[!] Nginx test failed!")
        sys.exit(1)

    print("[*] Reloading nginx on jp-server...")
    res_r = subprocess.run(['ssh', 'jp-server', 'systemctl reload nginx'], capture_output=True, text=True)
    if res_r.returncode != 0:
        print("[!] Nginx reload failed!")
        sys.exit(1)
    
    print("[+] jp-server Nginx HOT-RELOAD SUCCESSFUL!")

if __name__ == '__main__':
    main()
