"""
These tests depend on the availability of the starter project in `tests/demo`. Note
that during the CI a new model is trained at every run to ensure that we've got ourselves
a model file that we can use in these tests.
"""

import pathlib


from rasalit.apps.livenlu.common import (
    _mk_spacy_doc,
    load_interpreter,
    fetch_info_from_message,
)


def test_load_interpreter_can_load():
    model_folder = "tests/demo/models"
    model_path = list(pathlib.Path(model_folder).glob("*"))[0]
    interpreter = load_interpreter(model_folder, str(model_path.parts[-1]))
    blob, nlu_dict, tokens = fetch_info_from_message(
        interpreter=interpreter, text_input="hello world"
    )

    assert nlu_dict["text"] == "hello world"
    assert [t.text for t in nlu_dict["text_tokens"]] == ["hello", "world"]
    all_intents = [
        "talk_code",
        "bot_challenge",
        "mood_unhappy",
        "mood_great",
        "deny",
        "affirm",
        "goodbye",
        "greet",
    ]
    assert [i["name"] in all_intents for i in nlu_dict["intent_ranking"]]


def test_can_pick_up_entities():
    model_folder = "tests/demo/models"
    model_path = list(pathlib.Path(model_folder).glob("*"))[0]
    interpreter = load_interpreter(model_folder, str(model_path.parts[-1]))
    blob, nlu_dict, tokens = fetch_info_from_message(
        interpreter=interpreter, text_input="hello python"
    )
    assert nlu_dict["entities"][0]["entity"] == "proglang"
    assert nlu_dict["entities"][0]["value"] == "python"


def test_create_spacy_doc():
    tokens = ["Hello", "python", "and", "golang"]
    entities = [
        {
            "entity": "proglang",
            "start": 6,
            "end": 12,
            "value": "python",
            "extractor": "DIETClassifier",
        },
        {
            "entity": "proglang",
            "start": 17,
            "end": 23,
            "value": "golang",
            "extractor": "DIETClassifier",
        },
    ]
    doc = _mk_spacy_doc(tokens=tokens, entities=entities)
    for ent in doc.ents:
        assert ent.text in ["python", "golang"]
        assert ent.label_ == "proglang"
