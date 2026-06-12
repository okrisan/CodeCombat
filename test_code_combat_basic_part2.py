#!/usr/bin/env python3
"""Test base per Code Combat Parte 2 — incapsulamento e visibilità.

Verifica che il refactoring abbia:
- reso privati gli attributi chiave (name mangling con doppio underscore)
- introdotto i getter per gli attributi leggibili da fuori
- preservato il comportamento esterno della Parte 1 (equip, attack, is_alive,
  take_damage, __str__)

I test sui setter, sulla validazione e sulla trappola dell'assegnazione
vivono nel file _advanced.
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


# ---------- Struttura ----------

def test_structure_icebreaker():
    """Esiste il file icebreaker.py con la classe Icebreaker."""
    assert Icebreaker is not None, (
        "ERRORE CRITICO: non trovo la classe 'Icebreaker' in 'icebreaker.py'. "
        "Verifica che il file sia denominato esattamente 'icebreaker.py' "
        "e che la classe si chiami 'Icebreaker'."
    )


def test_structure_runner():
    """Esiste il file runner.py con la classe Runner."""
    assert Runner is not None, (
        "ERRORE CRITICO: non trovo la classe 'Runner' in 'runner.py'. "
        "Verifica che il file sia denominato esattamente 'runner.py' "
        "e che la classe si chiami 'Runner'."
    )


# ---------- Attributi privati: name mangling ----------

def test_icebreaker_attributes_are_private():
    """Gli attributi di Icebreaker hanno subito il name mangling."""
    ice = Icebreaker("Fracter Alfa", 5, 10, "fracter")
    assert hasattr(ice, "_Icebreaker__name"), (
        "Atteso attributo privato '__name' in Icebreaker (name mangling)."
    )
    assert hasattr(ice, "_Icebreaker__min_damage")
    assert hasattr(ice, "_Icebreaker__max_damage")
    assert hasattr(ice, "_Icebreaker__type")


def test_runner_attributes_are_private():
    """Gli attributi di Runner hanno subito il name mangling."""
    r = Runner("armitage", 50, 12, 10)
    assert hasattr(r, "_Runner__handle"), (
        "Atteso attributo privato '__handle' in Runner (name mangling)."
    )
    assert hasattr(r, "_Runner__integrity")
    assert hasattr(r, "_Runner__max_integrity")
    assert hasattr(r, "_Runner__power")
    assert hasattr(r, "_Runner__finesse")


# ---------- Getter ----------

def test_icebreaker_getters_return_correct_values():
    """I getter di Icebreaker restituiscono i valori passati al costruttore."""
    ice = Icebreaker("Decoder", 3, 7, "decoder")
    assert ice.get_name() == "Decoder"
    assert ice.get_min_damage() == 3
    assert ice.get_max_damage() == 7
    assert ice.get_type() == "decoder"


def test_runner_getters_return_initial_state():
    """I getter di Runner riflettono lo stato iniziale."""
    r = Runner("molly", 45, 8, 15)
    assert r.get_handle() == "molly"
    assert r.get_max_integrity() == 45
    assert r.get_integrity() == 45
    assert r.get_power() == 8
    assert r.get_finesse() == 15


# ---------- Comportamento pubblico invariato ----------

def test_get_damage_in_range():
    """get_damage continua a restituire interi nel range [min, max]."""
    ice = Icebreaker("Pipeline", 4, 9, "decoder")
    for _ in range(50):
        d = ice.get_damage()
        assert isinstance(d, int)
        assert 4 <= d <= 9, f"Atteso valore in [4,9], ottenuto {d}"


def test_runner_equip_and_get_icebreaker():
    """equip collega l'icebreaker; il getter lo restituisce."""
    r = Runner("case", 40, 10, 12)
    ice = Icebreaker("Glitch", 5, 10, "fracter")
    r.equip(ice)
    assert r.get_icebreaker() is ice


def test_runner_take_damage_decrements_integrity():
    """take_damage continua a sottrarre integrità."""
    r = Runner("wintermute", 30, 10, 10)
    r.take_damage(7)
    assert r.get_integrity() == 23


def test_runner_take_damage_does_not_go_below_zero():
    """take_damage non porta l'integrità sotto zero (invariante della Parte 1)."""
    r = Runner("ghost", 10, 10, 10)
    r.take_damage(100)
    assert r.get_integrity() == 0


def test_runner_is_alive_reflects_integrity():
    """is_alive resta True finché integrity > 0."""
    r = Runner("neuromancer", 20, 10, 10)
    assert r.is_alive() is True
    r.take_damage(20)
    assert r.is_alive() is False


def test_runner_str_contains_handle_and_integrity():
    """__str__ del Runner contiene handle e integrità corrente."""
    r = Runner("3jane", 25, 10, 10)
    s = str(r)
    assert "3jane" in s
    assert "25" in s


def test_icebreaker_str_contains_name_and_range():
    """__str__ dell'Icebreaker contiene nome e range di danno."""
    ice = Icebreaker("BlackIce", 6, 11, "fracter")
    s = str(ice)
    assert "BlackIce" in s
    assert "6" in s and "11" in s
