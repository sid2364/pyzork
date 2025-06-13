"""Simple fallback using a small language model to interpret free form commands."""

from __future__ import annotations

from typing import Optional

import grammar

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
_tokenizer = None
_model = None


def _load() -> None:
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _tokenizer.pad_token = _tokenizer.eos_token
        _model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        _model.to("cpu")


def suggest_command(user_text: str, player, game_map, gram) -> Optional[str]:
    """Return a best guess command string or ``None``.

    The player's inventory and current location description are provided to the
    language model as context.
    """
    _load()
    inventory = ", ".join(player.have) if player.have else "nothing"
    location = game_map.fsm.get(player.position, {})#.get("description", "")
    rules = []
    for i, rule in enumerate(gram.grammar):
        func = grammar.grammarToFunctionMap.get(i, "")
        joined = " ".join(str(x) for x in rule)
        rules.append(f"{func}: {joined}")
    grammar_text = "; ".join(rules)
    prompt = (
        "You are a command suggestion engine for a text adventure game. You need to give one single command, no more."
        " Some of the following are in JSON."
        "Use the following grammar for valid commands: "
        f"{grammar_text}\n"
        "Example command: 'walk east', 'take sword', 'fight dragon', 'look south'"
        f"Inventory: {inventory}\nLocation: {location}\n"
        f"User command: {user_text}\nGame command:"
    )
    inputs = _tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True
    )
    with torch.no_grad():
        outputs = _model.generate(
            input_ids=inputs.input_ids,
            attention_mask=inputs.attention_mask,
            pad_token_id=_tokenizer.eos_token_id,
            eos_token_id=_tokenizer.eos_token_id,
            max_new_tokens=8,
            do_sample=True,
            top_k=50,
            temperature=0.7,
            no_repeat_ngram_size=2,
            repetition_penalty=1.2,
        )
    generated = _tokenizer.decode(outputs[0], skip_special_tokens=True)
    suggestion = generated[len(prompt) :].strip().split("\n")[0]

    print("genrated", generated)
    print("suggestion", suggestion)
    print(f"You hear a faint voice from the skies... Did you mean '{suggestion}'?")

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
