from unittest.mock import patch

import pytest
import torch
from torch import Tensor
from transformers import (
    AutoModelForCausalLM,
    AutoModelForMaskedLM,
    AutoModelForPreTraining,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
)
from transformers_interpret import BaseExplainer

DISTILBERT_MODEL = AutoModelForMaskedLM.from_pretrained("distilbert-base-uncased")
DISTILBERT_TOKENIZER = AutoTokenizer.from_pretrained("distilbert-base-uncased")

GPT2_MODEL = AutoModelForCausalLM.from_pretrained("sshleifer/tiny-gpt2")
GPT2_TOKENIZER = AutoTokenizer.from_pretrained("sshleifer/tiny-gpt2")

BERT_MODEL = AutoModelForPreTraining.from_pretrained("lysandre/tiny-bert-random")
BERT_TOKENIZER = AutoTokenizer.from_pretrained("lysandre/tiny-bert-random")


class DummyExplainer(BaseExplainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def encode(self, text: str = None):
        if text is None:
            text = self.text
        return self.tokenizer.encode(text, add_special_tokens=False)

    def decode(self, input_ids):
        return self.tokenizer.convert_ids_to_tokens(input_ids[0])

    def _run(self):
        pass

    def _calculate_attributions(self):
        pass

    def _forward(self):
        pass


def test_explainer_init_distilbert():
    explainer = DummyExplainer("testing", DISTILBERT_MODEL, DISTILBERT_TOKENIZER)
    assert explainer.text == "testing"
    assert isinstance(explainer.model, PreTrainedModel)
    assert isinstance(explainer.tokenizer, PreTrainedTokenizerFast) | isinstance(
        explainer.tokenizer, PreTrainedTokenizer
    )
    assert explainer.model_prefix == DISTILBERT_MODEL.base_model_prefix
    if torch.cuda.is_available():
        assert explainer.device.type == "cuda:0"
    else:
        assert explainer.device.type == "cpu"

    assert explainer.accepts_position_ids == False
    assert explainer.accepts_token_type_ids == False

    assert explainer.model.config.model_type == "distilbert"
    assert explainer.position_embeddings != None
    assert explainer.word_embeddings != None
    assert explainer.token_type_embeddings == None


def test_explainer_init_bert():
    explainer = DummyExplainer("testing", BERT_MODEL, BERT_TOKENIZER)
    assert explainer.text == "testing"
    assert isinstance(explainer.model, PreTrainedModel)
    assert isinstance(explainer.tokenizer, PreTrainedTokenizerFast) | isinstance(
        explainer.tokenizer, PreTrainedTokenizer
    )
    assert explainer.model_prefix == BERT_MODEL.base_model_prefix
    if torch.cuda.is_available():
        assert explainer.device.type == "cuda:0"
    else:
        assert explainer.device.type == "cpu"

    assert explainer.accepts_position_ids == True
    assert explainer.accepts_token_type_ids == True

    assert explainer.model.config.model_type == "bert"
    assert explainer.position_embeddings != None
    assert explainer.word_embeddings != None
    assert explainer.token_type_embeddings != None


def test_explainer_init_gpt2():
    explainer = DummyExplainer("testing", GPT2_MODEL, GPT2_TOKENIZER)
    assert explainer.text == "testing"
    assert isinstance(explainer.model, PreTrainedModel)
    assert isinstance(explainer.tokenizer, PreTrainedTokenizerFast) | isinstance(
        explainer.tokenizer, PreTrainedTokenizer
    )
    assert explainer.model_prefix == GPT2_MODEL.base_model_prefix
    if torch.cuda.is_available():
        assert explainer.device.type == "cuda:0"
    else:
        assert explainer.device.type == "cpu"

    assert explainer.accepts_position_ids == True
    assert explainer.accepts_token_type_ids == True

    assert explainer.model.config.model_type == "gpt2"
    assert explainer.position_embeddings != None
    assert explainer.word_embeddings != None


def test_explainer_make_input_reference_pair():
    explainer = DummyExplainer(
        "this is a test string", DISTILBERT_MODEL, DISTILBERT_TOKENIZER
    )
    input_ids, ref_input_ids, len_inputs = explainer._make_input_reference_pair(
        "this is a test string"
    )
    assert isinstance(input_ids, Tensor)
    assert isinstance(ref_input_ids, Tensor)
    assert isinstance(len_inputs, int)

    assert len(input_ids[0]) == len(ref_input_ids[0]) == (len_inputs + 2)
    assert ref_input_ids[0][0] == input_ids[0][0]
    assert ref_input_ids[0][-1] == input_ids[0][-1]
    assert ref_input_ids[0][0] == explainer.cls_token_id
    assert ref_input_ids[0][-1] == explainer.sep_token_id


def test_explainer_make_input_reference_pair_gpt2():
    explainer = DummyExplainer("this is a test string", GPT2_MODEL, GPT2_TOKENIZER)
    input_ids, ref_input_ids, len_inputs = explainer._make_input_reference_pair(
        "this is a test string"
    )
    assert isinstance(input_ids, Tensor)
    assert isinstance(ref_input_ids, Tensor)
    assert isinstance(len_inputs, int)

    assert len(input_ids[0]) == len(ref_input_ids[0]) == (len_inputs)


def test_explainer_make_input_token_type_pair_no_sep_idx():
    explainer = DummyExplainer(
        "this is a test string", DISTILBERT_MODEL, DISTILBERT_TOKENIZER
    )
    input_ids, ref_input_ids, len_inputs = explainer._make_input_reference_pair(
        "this is a test string"
    )
    (
        token_type_ids,
        ref_token_type_ids,
    ) = explainer._make_input_reference_token_type_pair(input_ids)

    assert ref_token_type_ids[0][0] == torch.zeros(len(input_ids[0]))[0]
    for i, val in enumerate(token_type_ids[0]):
        if i == 0:
            assert val == 0
        else:
            assert val == 1


def test_explainer_make_input_token_type_pair_sep_idx():
    explainer = DummyExplainer(
        "this is a test string", DISTILBERT_MODEL, DISTILBERT_TOKENIZER
    )
    input_ids, ref_input_ids, len_inputs = explainer._make_input_reference_pair(
        "this is a test string"
    )
    (
        token_type_ids,
        ref_token_type_ids,
    ) = explainer._make_input_reference_token_type_pair(input_ids, 3)

    assert ref_token_type_ids[0][0] == torch.zeros(len(input_ids[0]))[0]
    for i, val in enumerate(token_type_ids[0]):
        if i <= 3:
            assert val == 0
        else:
            assert val == 1


def test_explainer_make_input_reference_position_id_pair():
    explainer = DummyExplainer(
        "this is a test string", DISTILBERT_MODEL, DISTILBERT_TOKENIZER
    )
    input_ids, ref_input_ids, len_inputs = explainer._make_input_reference_pair(
        "this is a test string"
    )
    position_ids, ref_position_ids = explainer._make_input_reference_position_id_pair(
        input_ids
    )

    assert ref_position_ids[0][0] == torch.zeros(len(input_ids[0]))[0]
    for i, val in enumerate(position_ids[0]):
        assert val == i


def test_explainer_make_attention_mask():
    explainer = DummyExplainer(
        "this is a test string", DISTILBERT_MODEL, DISTILBERT_TOKENIZER
    )
    input_ids, ref_input_ids, len_inputs = explainer._make_input_reference_pair(
        "this is a test string"
    )
    attention_mask = explainer._make_attention_mask(input_ids)
    assert len(attention_mask[0]) == len(input_ids[0])
    for i, val in enumerate(attention_mask[0]):
        assert val == 1


def test_explainer_str():
    test_string = "this is a test string"
    explainer = DummyExplainer(test_string, DISTILBERT_MODEL, DISTILBERT_TOKENIZER)
    s = "DummyExplainer("
    s += f'\n\ttext="{test_string[:10]}...",'
    s += f"\n\tmodel={DISTILBERT_MODEL.__class__.__name__},"
    s += f"\n\ttokenizer={DISTILBERT_TOKENIZER.__class__.__name__}"
    s += ")"
    assert s == explainer.__str__()
