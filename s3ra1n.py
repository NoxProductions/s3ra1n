#!/usr/bin/env python3
import subprocess
import sys
import os
import time

# ── ANSI COLORS ──────────────────────────────────────────────────────────────
R  = "\033[38;5;196m"   # red
V  = "\033[38;5;135m"   # violet
B  = "\033[38;5;39m"    # blue
LB = "\033[38;5;75m"    # light blue
W  = "\033[97m"         # white
DIM= "\033[38;5;240m"   # dim gray
YL = "\033[38;5;220m"   # yellow
GR = "\033[38;5;83m"    # green
RST= "\033[0m"          # reset
BOLD="\033[1m"

# ── ASCII BANNER ──────────────────────────────────────────────────────────────
BANNER = f"""
{V}        .:'                    
{V}    __ :'__                   
{B} .'`__`-'__``.               {W+BOLD} s3ra1n {RST+DIM}v2.2.0 — Universal ARMv7{RST}
{B}:__________.-'               {DIM} An experimental Ra1n Project{RST}
{R}:_________:                  {DIM} github.com/noxbitx/s3ra1n{RST}
{R} :_________`-;              
{V}  `.___.-.__.'               {DIM} palera1n wrapper for ARMv7 Linux{RST}
"""

DIVIDER = f"{DIM}{'─' * 52}{RST}"

# ── PALERA1N BINARY ───────────────────────────────────────────────────────────
def find_palera1n():
    # Quick candidates first
    candidates = [
        "/usr/local/bin/palera1n",
        "/usr/bin/palera1n",
        "/tmp/palera1n",
        "/tmp/palera1n-v221-armel",
    ]
    for path in candidates:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    # Deep search: walk common dirs, skip palera1n-c source folders
    search_roots = [
        os.path.expanduser("~"),
        "/tmp",
        "/opt",
        "/usr/local",
    ]
    for root in search_roots:
        for dirpath, dirnames, filenames in os.walk(root):
            # Skip palera1n-c source tree (has a Makefile + src/ subfolder)
            if "Makefile" in filenames and "src" in dirnames:
                dirnames[:] = []
                continue
            # Skip hidden dirs and venvs
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'venv']
            for fname in filenames:
                if fname == "palera1n" or fname.startswith("palera1n-linux"):
                    full = os.path.join(dirpath, fname)
                    if os.access(full, os.X_OK):
                        return full
    return None

def splash_search():
    os.system("clear")
    print(f"""
{V}        .:'
{V}    __ :'__
{B} .'`__`-'__``.
{B}:__________.-'
{R}:_________:
{R} :_________`-;
{V}  `.___.-.__.'
""")
    print(DIVIDER)
    print(f"\n  {DIM}Searching for palera1n, please wait...{RST}\n")

    # Animated dots
    for i in range(3):
        print(f"  {B}{'.' * (i+1)}{RST}", end="\r", flush=True)
        time.sleep(0.4)

    result = find_palera1n()

    if result:
        print(f"  {GR}✓ Found!{RST} {DIM}{result}{RST}          ")
        print(f"\n  {W}Redirecting in...{RST}")
        for i in range(3, 0, -1):
            print(f"  {B}{i}...{RST}", end="\r", flush=True)
            time.sleep(1)
    else:
        print(f"  {R}✗ palera1n not found!{RST}          ")
        print(f"\n  {DIM}Download from: https://github.com/noxbitx/s3ra1n/releases{RST}")
        print(f"  {DIM}Place binary anywhere in ~ or /tmp and re-run.{RST}\n")
        print(DIVIDER)
        input(f"\n  {DIM}Press Enter to exit...{RST}")
        sys.exit(1)

    return result

PALERA1N = splash_search()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def clear():
    os.system("clear")

def print_banner():
    clear()
    print(BANNER)
    print(DIVIDER)

    if PALERA1N:
        print(f"  {GR}●{RST} palera1n found: {DIM}{PALERA1N}{RST}")
    else:
        print(f"  {R}●{RST} palera1n {R}not found{RST} — place binary at ~/palera1n")
    print(DIVIDER)

def kill_usbmuxd():
    print(f"\n{DIM}  → Killing usbmuxd...{RST}")
    subprocess.run(["sudo", "killall", "usbmuxd"], stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "rm", "-f", "/var/run/usbmuxd"], stderr=subprocess.DEVNULL)
    time.sleep(0.5)
    print(f"  {GR}✓{RST} usbmuxd cleared")

def start_usbmuxd():
    print(f"\n{DIM}  → Starting usbmuxd...{RST}")
    subprocess.Popen(["sudo", "usbmuxd", "-f"], stderr=subprocess.DEVNULL)
    time.sleep(1)
    print(f"  {GR}✓{RST} usbmuxd started")

def run_palera1n(flags: list, description: str):
    if not PALERA1N:
        print(f"\n  {R}✗ palera1n binary not found.{RST}")
        print(f"  {DIM}Download from: https://github.com/noxbitx/s3ra1n/releases{RST}\n")
        input(f"  {DIM}Press Enter to go back...{RST}")
        return

    print_banner()
    print(f"\n  {B}▶ {W+BOLD}{description}{RST}")
    print(f"  {DIM}Command: sudo {PALERA1N} {' '.join(flags)}{RST}\n")
    print(DIVIDER)

    kill_usbmuxd()

    print(f"\n  {YL}⚡ Starting palera1n...{RST}\n")
    print(DIVIDER + "\n")

    try:
        subprocess.run(["sudo", PALERA1N] + flags)
    except KeyboardInterrupt:
        print(f"\n\n  {YL}⚠ Interrupted by user{RST}")

    print(f"\n{DIVIDER}")
    input(f"\n  {DIM}Press Enter to return to menu...{RST}")

def confirm(msg: str) -> bool:
    ans = input(f"\n  {YL}⚠ {msg} [{W}y{RST}/{YL}n{RST}]: ").strip().lower()
    return ans == 'y'

def download_palera1n():
    print_banner()
    print(f"\n  {B}▶ {W+BOLD}Download palera1n-linux-armel{RST}\n")
    print(f"  {DIM}Fetching latest release...{RST}\n")

    dest = os.path.expanduser("~/palera1n")
    url = "https://github.com/palera1n/palera1n/releases/download/v2.2.1/palera1n-linux-armel"

    try:
        subprocess.run(["curl", "-L", url, "-o", dest, "--progress-bar"], check=True)
        subprocess.run(["chmod", "+x", dest])
        print(f"\n  {GR}✓ Downloaded to {dest}{RST}")
        global PALERA1N
        PALERA1N = dest
    except Exception as e:
        print(f"\n  {R}✗ Download failed: {e}{RST}")

    input(f"\n  {DIM}Press Enter to return to menu...{RST}")

# ── MENU ITEMS ────────────────────────────────────────────────────────────────
MENU = [
    # (label, flags, description, confirm_msg or None)
    (
        f"{GR}Jailbreak{RST}              Rootful {DIM}(-f){RST}",
        ["-f"],
        "Rootful Jailbreak",
        None
    ),
    (
        f"{GR}Jailbreak{RST}              Rootless {DIM}(-l){RST}",
        ["-l"],
        "Rootless Jailbreak",
        None
    ),
    (
        f"{YL}Setup{RST}                  Create fakefs {DIM}(-f -B){RST}",
        ["-f", "-B"],
        "Create FakeFS (first-time rootful setup)",
        None
    ),
    (
        f"{YL}Setup{RST}                  Create partial fakefs {DIM}(-f --setup-partial-fakefs){RST}",
        ["-f", "--setup-partial-fakefs"],
        "Create Partial FakeFS",
        None
    ),
    (
        f"{B}Boot{RST}                   PongoOS shell {DIM}(--pongo-shell){RST}",
        ["--pongo-shell"],
        "Boot into PongoOS shell",
        None
    ),
    (
        f"{B}Boot{RST}                   Verbose boot {DIM}(-f --verbose-boot){RST}",
        ["-f", "--verbose-boot"],
        "Rootful Jailbreak with verbose boot",
        None
    ),
    (
        f"{B}Boot{RST}                   Safe mode {DIM}(-f --safe-mode){RST}",
        ["-f", "--safe-mode"],
        "Rootful Jailbreak in safe mode",
        None
    ),
    (
        f"{B}Recovery{RST}               Enter recovery mode {DIM}(--enter-recovery){RST}",
        ["--enter-recovery"],
        "Enter Recovery Mode",
        None
    ),
    (
        f"{B}Recovery{RST}               Exit recovery mode {DIM}(--exit-recovery){RST}",
        ["--exit-recovery"],
        "Exit Recovery Mode",
        None
    ),
    (
        f"{V}Info{RST}                   Device info {DIM}(--device-info){RST}",
        ["--device-info"],
        "Show Device Info",
        None
    ),
    (
        f"{R}Danger{RST}                 Force revert jailbreak {DIM}(--force-revert){RST}",
        ["--force-revert"],
        "Force Revert Jailbreak",
        "This will REMOVE the jailbreak. Are you sure?"
    ),
    (
        f"{DIM}Tools{RST}                  Start usbmuxd only",
        None,
        "Start usbmuxd",
        None
    ),
    (
        f"{DIM}Tools{RST}                  Kill usbmuxd only",
        None,
        "Kill usbmuxd",
        None
    ),
    (
        f"{DIM}Tools{RST}                  Download palera1n binary",
        None,
        "Download palera1n",
        None
    ),
]

# ── MAIN LOOP ─────────────────────────────────────────────────────────────────
def main():
    while True:
        print_banner()
        print(f"\n  {W+BOLD}Select an option:{RST}\n")

        for i, (label, _, _, _) in enumerate(MENU, 1):
            num = f"{DIM}{i:>2}.{RST}"
            print(f"  {num}  {label}")

        print(f"\n  {DIM} 0.  Exit{RST}")
        print(f"\n{DIVIDER}")

        try:
            choice = input(f"\n  {B}s3ra1n{RST} {DIM}›{RST} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n  {DIM}bye o/{RST}\n")
            sys.exit(0)

        if choice == "0":
            print(f"\n  {DIM}bye o/{RST}\n")
            sys.exit(0)

        if not choice.isdigit() or not (1 <= int(choice) <= len(MENU)):
            print(f"\n  {R}✗ Invalid option{RST}")
            time.sleep(0.8)
            continue

        idx = int(choice) - 1
        label, flags, description, confirm_msg = MENU[idx]

        # Special cases (no flags = tool actions)
        if flags is None:
            if "usbmuxd only" in description and "Start" in description:
                print_banner()
                start_usbmuxd()
                input(f"\n  {DIM}Press Enter to return...{RST}")
            elif "Kill" in description:
                print_banner()
                kill_usbmuxd()
                input(f"\n  {DIM}Press Enter to return...{RST}")
            elif "Download" in description:
                download_palera1n()
            continue

        # Confirmation for dangerous actions
        if confirm_msg:
            print_banner()
            if not confirm(confirm_msg):
                continue

        run_palera1n(flags, description)

if __name__ == "__main__":
    main()
