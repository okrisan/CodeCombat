#!/usr/bin/env python3
"""Test avanzati per Code Combat Parte 2 — incapsulamento e visibilità.

Coprono i casi limite e le proprietà critiche del refactoring:
- la "trappola dell'assegnazione": scrivere obj.__x da fuori non altera lo stato
- la validazione nei setter di Icebreaker (input non interi, valori negativi,
  invariante min_damage <= max_damage)
- l'assenza di un setter generico per Runner.__integrity
  (Tell, don't ask: si modifica solo via take_damage / heal)
- il comportamento di take_damage con valori limite (negativi, zero, oltre il max)
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


# ---------- La trappola dell'assegnazione ----------

def test_assignment_trap_runner_integrity():
    """Scrivere r.__integrity da fuori non modifica il vero attributo privato.

    Python crea un attributo pubblico spazzatura sull'istanza, ma _Runner__integrity
    resta intatto e get_integrity() continua a restituire il valore originale.
    """
    r = Runner("armitage", 50, 12, 10)
    r.__integrity = -9999   # tentativo di scrittura "da fuori"
    assert r.get_integrity() == 50, (
        "L'attributo privato __integrity NON deve essere modificato dall'esterno. "
        "Se questo test fallisce, l'attributo non è realmente privato (manca il "
        "doppio underscore davanti, o c'è un setter pubblico che non dovrebbe esserci)."
    )
    assert r._Runner__integrity == 50


def test_assignment_trap_icebreaker_min_damage():
    """Stesso principio per Icebreaker: __min_damage da fuori non si scrive."""
    ice = Icebreaker("Fracter", 5, 10, "fracter")
    ice.__min_damage = 9999
    assert ice.get_min_damage() == 5
    assert ice._Icebreaker__min_damage == 5


# ---------- Setter di Icebreaker: validazione ----------

def test_set_min_damage_rejects_non_int():
    """set_min_damage non accetta valori non interi (non altera lo stato)."""
    ice = Icebreaker("Decoder", 3, 7, "decoder")
    ice.set_min_damage("molto")
    assert ice.get_min_damage() == 3, (
        "set_min_damage deve rifiutare valori non interi senza alterare lo stato."
    )


def test_set_min_damage_rejects_negative():
    """set_min_damage non lascia mai min_damage negativo."""
    ice = Icebreaker("Decoder", 3, 7, "decoder")
    ice.set_min_damage(-5)
    assert ice.get_min_damage() >= 0, (
        "Dopo set_min_damage(-5), min_damage NON deve essere negativo."
    )


def test_set_min_damage_preserves_invariant():
    """min_damage non può superare max_damage (invariante)."""
    ice = Icebreaker("Decoder", 3, 7, "decoder")
    ice.set_min_damage(100)
    assert ice.get_min_damage() <= ice.get_max_damage(), (
        "Dopo un set_min_damage che sfora max_damage, l'invariante "
        "min_damage <= max_damage deve restare valido."
    )


def test_set_max_damage_preserves_invariant():
    """max_damage non può scendere sotto min_damage."""
    ice = Icebreaker("Decoder", 5, 10, "decoder")
    ice.set_max_damage(1)
    assert ice.get_max_damage() >= ice.get_min_damage(), (
        "Dopo un set_max_damage che va sotto min_damage, l'invariante "
        "min_damage <= max_damage deve restare valido."
    )


def test_icebreaker_name_is_read_only():
    """Non deve esistere set_name su Icebreaker (read-only)."""
    ice = Icebreaker("Fracter", 5, 10, "fracter")
    assert not hasattr(ice, "set_name"), (
        "Icebreaker.set_name NON deve esistere: il nome è read-only dopo la creazione."
    )


def test_icebreaker_type_is_read_only():
    """Non deve esistere set_type su Icebreaker (read-only)."""
    ice = Icebreaker("Fracter", 5, 10, "fracter")
    assert not hasattr(ice, "set_type"), (
        "Icebreaker.set_type NON deve esistere: il tipo è read-only dopo la creazione."
    )


# ---------- Runner: no setter generico per integrity ----------

def test_runner_no_generic_integrity_setter():
    """Non deve esistere set_integrity: si modifica solo via take_damage / heal."""
    r = Runner("molly", 45, 8, 15)
    assert not hasattr(r, "set_integrity"), (
        "Runner.set_integrity NON deve esistere. Modifica __integrity solo tramite "
        "metodi semantici (take_damage, heal). Principio: Tell, don't ask."
    )


def test_runner_handle_is_read_only():
    """Non deve esistere set_handle su Runner."""
    r = Runner("molly", 45, 8, 15)
    assert not hasattr(r, "set_handle")


def test_runner_max_integrity_is_read_only():
    """Non deve esistere set_max_integrity su Runner."""
    r = Runner("molly", 45, 8, 15)
    assert not hasattr(r, "set_max_integrity")


# ---------- take_damage: invarianti ai bordi ----------

def test_take_damage_overshoot_clamps_to_zero():
    """take_damage con danno > integrity fissa integrity a 0, non a negativo."""
    r = Runner("case", 20, 10, 10)
    r.take_damage(1000)
    assert r.get_integrity() == 0


def test_take_damage_zero_does_not_change_state():
    """take_damage(0) non altera lo stato."""
    r = Runner("case", 20, 10, 10)
    before = r.get_integrity()
    r.take_damage(0)
    assert r.get_integrity() == before


def test_take_damage_multiple_calls_cumulative():
    """Più chiamate consecutive di take_damage si sommano correttamente."""
    r = Runner("case", 30, 10, 10)
    r.take_damage(5)
    r.take_damage(7)
    r.take_damage(3)
    assert r.get_integrity() == 30 - 5 - 7 - 3


# ---------- Independenza fra istanze ----------

def test_two_runners_have_independent_state():
    """Modificare un Runner non tocca l'altro."""
    a = Runner("armitage", 50, 12, 10)
    m = Runner("molly", 45, 8, 15)
    a.take_damage(20)
    assert a.get_integrity() == 30
    assert m.get_integrity() == 45, (
        "I due Runner devono avere stato indipendente. "
        "Se modificare 'a' tocca 'm', l'attributo è stato definito come "
        "variabile di classe invece che di istanza."
    )


# ---------- get_damage: range rispettato anche con range collassato ----------

def test_get_damage_with_equal_min_max():
    """Se min_damage == max_damage, get_damage restituisce sempre quel valore."""
    ice = Icebreaker("Stunlock", 8, 8, "decoder")
    for _ in range(20):
        assert ice.get_damage() == 8
