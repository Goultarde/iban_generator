#!/usr/bin/env python3
"""Génère des IBAN français de test valides au contrôle modulo 97."""

import argparse
import secrets

BANK_BRANCHES = (
    ("20041", "01005"),
    ("30002", "00495"),
    ("30003", "00050"),
    ("30004", "00961"),
)


def generate_iban() -> str:
    bank, branch = secrets.choice(BANK_BRANCHES)
    account = f"{secrets.randbelow(10**11):011d}"
    rib_key = 97 - (89 * int(bank) + 15 * int(branch) + 3 * int(account)) % 97
    bban = f"{bank}{branch}{account}{rib_key:02d}"
    iban_key = 98 - int(f"{bban}152700") % 97  # F=15, R=27, clé provisoire=00
    iban = f"FR{iban_key:02d}{bban}"
    assert int(f"{iban[4:]}1527{iban[2:4]}") % 97 == 1
    return iban


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("count", nargs="?", type=int, default=1, help="nombre d'IBAN à générer")
    args = parser.parse_args()
    if args.count < 1:
        parser.error("count doit être supérieur à 0")
    for _ in range(args.count):
        print(generate_iban())
