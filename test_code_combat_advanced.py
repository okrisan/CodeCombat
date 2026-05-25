#!/usr/bin/env python3
"""Test avanzati per Code Combat Parte 1.

Coprono validazioni di coerenza, edge cases di take_damage e la logica di attack:
scelta del modificatore in base al tipo di icebreaker, floor a zero, fallback
senza arma.
"""

import pytest

try:
    from icebreaker import Icebreaker
except ImportError:
    Icebreaker = None

try:
    from runner import Runner
except ImportError:
    Runner = None


# ---------- Validazioni del costruttore ----------

def test_icebreaker_min_damage_at_least_1(capsys):
    """min_damage < 1 deve produrre un avviso (non un crash)."""
    if Icebreaker is None:
        pytest.skip("Icebreaker non disponibile")
    ice = Icebreaker("Broken", 0, 5, "fracter")
    captured = capsys.readouterr()
    # niente assert sul valore esatto: basta che il codice non crashi
    assert ice.min_damage >= 1 or "ATTENZIONE" in captured.out or "warn" in captured.out.lower()


def test_icebreaker_max_lower_than_min(capsys):
    """Se max_damage < min_damage, il range deve essere corretto a uno coerente."""
    ice = Icebreaker("Inverted", 10, 3, "fracter")
    assert ice.max_damage >= ice.min_damage, (
        f"Atteso max_damage >= min_damage dopo correzione, "
        f"ottenuto min={ice.min_damage} max={ice.max_damage}"
    )


def test_icebreaker_invalid_type(capsys):
    """Un tipo non valido viene segnalato e ricondotto a un default consentito."""
    ice = Icebreaker("Unknown", 5, 10, "missile")
    assert ice.type in ("fracter", "decoder"), (
        f"Tipo non valido non corretto: {ice.type}"
    )


# ---------- take_damage edge cases ----------

def test_take_damage_never_below_zero():
    """L'integrity non scende mai sotto zero."""
    r = Runner("low", 10, 10, 10)
    applied = r.take_damage(50)
    assert r.integrity == 0
    assert applied == 10, f"Atteso danno effettivo 10, ottenuto {applied}"


def test_take_damage_negative_amount_is_zero():
    """Un danno negativo non cura il Runner."""
    r = Runner("safe", 20, 10, 10)
    initial = r.integrity
    applied = r.take_damage(-5)
    assert r.integrity == initial, "Un danno negativo non deve curare"
    assert applied == 0


# ---------- modifier ----------

def test_modifier_formula():
    """modifier(value) = (value - 10) // 2 (d20-style)."""
    r = Runner("calc", 10, 10, 10)
    assert r.modifier(10) == 0
    assert r.modifier(16) == 3
    assert r.modifier(8) == -1
    assert r.modifier(1) == -5
    assert r.modifier(20) == 5


# ---------- attack ----------

def test_attack_without_icebreaker():
    """Senza icebreaker il danno base è 1 (più il modificatore: deve restare >= 0)."""
    attacker = Runner("naked", 30, 10, 10)  # power=10 → modifier=0
    target = Runner("victim", 30, 10, 10)
    dealt = attacker.attack(target)
    assert dealt >= 0
    assert target.integrity == 30 - dealt


def test_attack_uses_power_for_fracter(monkeypatch):
    """Un icebreaker 'fracter' somma il modificatore di power, non di finesse."""
    attacker = Runner("brute", 30, 18, 1)   # power=18 → +4 ; finesse=1 → -5
    target = Runner("dummy", 100, 10, 10)
    ice = Icebreaker("BlackIce", 10, 10, "fracter")  # range collassato a 10
    attacker.equip(ice)
    dealt = attacker.attack(target)
    # 10 (base) + 4 (modifier power) = 14
    assert dealt == 14, f"Atteso 14, ottenuto {dealt}"


def test_attack_uses_finesse_for_decoder():
    """Un icebreaker 'decoder' somma il modificatore di finesse."""
    attacker = Runner("ghost", 30, 1, 18)   # power=1 → -5 ; finesse=18 → +4
    target = Runner("dummy", 100, 10, 10)
    ice = Icebreaker("Pipeline", 10, 10, "decoder")
    attacker.equip(ice)
    dealt = attacker.attack(target)
    assert dealt == 14, f"Atteso 14, ottenuto {dealt}"


def test_attack_damage_floor_at_zero():
    """Modificatore molto negativo non deve far andare il danno sotto 0."""
    attacker = Runner("weak", 30, 1, 1)   # entrambe le stat al minimo → modifier=-5
    target = Runner("dummy", 30, 10, 10)
    ice = Icebreaker("Tiny", 1, 1, "fracter")  # base 1, modificatore -5 → totale teorico -4
    attacker.equip(ice)
    integrity_before = target.integrity
    dealt = attacker.attack(target)
    assert dealt >= 0, f"Il danno effettivo non può essere negativo, era {dealt}"
    assert target.integrity == integrity_before - dealt
