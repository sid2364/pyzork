"""Simple fallback using a small language model to interpret free form commands."""

from __future__ import annotations

from typing import Optional

import grammar

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

_MODEL_NAME = "sshleifer/tiny-gpt2"
_tokenizer = None
_model = None


def _load() -> None:
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)
        _model = AutoModelForCausalLM.from_pretrained(_MODEL_NAME)
        _model.to("cpu")


def suggest_command(user_text: str, player, game_map, gram) -> Optional[str]:
    """Return a best guess command string or ``None``.

    The player's inventory and current location description are provided to the
    language model as context.
    """
    _load()
    inventory = ", ".join(player.have) if player.have else "nothing"
    location = game_map.fsm.get(player.position, {}).get("description", "")
    rules = []
    for i, rule in enumerate(gram.grammar):
        func = grammar.grammarToFunctionMap.get(i, "")
        joined = " ".join(str(x) for x in rule)
        rules.append(f"{func}: {joined}")
    grammar_text = "; ".join(rules)
    prompt = (
        "You are a command suggestion engine for a text adventure game. "
        "Use the following grammar for valid commands: "
        f"{grammar_text}\n"
        f"Inventory: {inventory}\nLocation: {location}\n"
        f"User command: {user_text}\nGame command (few words):"
    )
    inputs = _tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = _model.generate(inputs, max_new_tokens=8)
    generated = _tokenizer.decode(outputs[0], skip_special_tokens=True)
    suggestion = generated[len(prompt) :].strip().split("\n")[0]

    fn, _ = gram.getGrammarType(suggestion)
    if fn is not None:
        return suggestion

    heuristics = {
        "rising sun": "go east",
        "setting sun": "go west",
    }
    for key, cmd in heuristics.items():
        if key in user_text.lower():
            return cmd

    return None
