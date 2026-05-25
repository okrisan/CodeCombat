#!/usr/bin/env python3
"""Test base per Code Combat Parte 1.

Verifica la struttura del progetto, la creazione delle istanze e i metodi base
di Icebreaker e Runner. NON copre la logica di attacco con modificatori, che vive
nel file _advanced.
"""

import random

import pytest

try:
    from icebreaker import Icebreaker
except ImportError:
    Icebreaker = None

try:
    from runner import Runner
except ImportError:
    Runner = None


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


def test_icebreaker_attributes():
    """L'Icebreaker espone name, min_damage, max_damage, type."""
    ice = Icebreaker("Fracter Alfa", 5, 10, "fracter")
    assert ice.name == "Fracter Alfa"
    assert ice.min_damage == 5
    assert ice.max_damage == 10
    assert ice.type == "fracter"


def test_icebreaker_get_damage_in_range():
    """get_damage restituisce un intero nel range richiesto."""
    ice = Icebreaker("Decoder", 3, 7, "decoder")
    for _ in range(50):
        d = ice.get_damage()
        assert isinstance(d, int)
        assert 3 <= d <= 7, f"Atteso valore in [3,7], ottenuto {d}"


def test_runner_initial_state():
    """Il Runner inizia con integrity == max_integrity e nessun icebreaker."""
    r = Runner("armitage", 50, 12, 10)
    assert r.handle == "armitage"
    assert r.max_integrity == 50
    assert r.integrity == 50
    assert r.power == 12
    assert r.finesse == 10
    assert r.icebreaker is None


def test_runner_equip():
    """equip() collega l'icebreaker al Runner."""
    r = Runner("molly", 40, 8, 15)
    ice = Icebreaker("Pipeline", 4, 9, "decoder")
    r.equip(ice)
    assert r.icebreaker is ice


def test_runner_is_alive():
    """is_alive riflette il valore di integrity."""
    r = Runner("ghost", 10, 10, 10)
    assert r.is_alive() is True
    r.integrity = 0
    assert r.is_alive() is False


def test_runner_take_damage_basic():
    """take_damage sottrae il danno e lo restituisce."""
    r = Runner("case", 30, 10, 10)
    applied = r.take_damage(7)
    assert applied == 7
    assert r.integrity == 23


def test_runner_str_contains_handle_and_hp():
    """__str__ del Runner contiene handle, integrity e max_integrity."""
    r = Runner("wintermute", 25, 10, 10)
    s = str(r)
    assert "wintermute" in s
    assert "25" in s


def test_icebreaker_str_contains_name_and_range():
    """__str__ dell'Icebreaker contiene nome e range di danno."""
    ice = Icebreaker("Glitch", 6, 11, "fracter")
    s = str(ice)
    assert "Glitch" in s
    assert "6" in s and "11" in s
