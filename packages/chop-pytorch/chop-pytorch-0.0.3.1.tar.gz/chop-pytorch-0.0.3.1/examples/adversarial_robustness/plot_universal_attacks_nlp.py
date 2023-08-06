"""
Universal Adversarial Attacks on NLP Models
===========================================

This example implements a universal adversarial attack on a sentiment analysis model.
The model is a pretrained sentiment analysis model from huggingface, based on BERT.

The threat model is the following: we append the same K tokens at the beginning of the inputs.
We then optimize over these K tokens to flip as many predictions as possible.
"""

# %%
import torch
from torch import nn
from torch.nn import Embedding
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from datasets import load_dataset


model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)


# %%
class GetGradientHook:
    def __init__(self):
        self.gradients = []

    def __call__(self, module, grad_in, grad_out):
        self.gradients.append(grad_out[0])


class TriggeredEmbeddingLayer(nn.Module):
    def __init__(self, embedding_layer, n_trigger_tokens):
        matrix = embedding_layer.weight
        super(TriggeredEmbeddingLayer, self).__init__()


def get_embedding_layer(model):
    for module in model.modules():
        if isinstance(module, Embedding):
            # check that module is the word embedding
            if module.num_embeddings > 1e5:
                embedding_layer = module
    return embedding_layer


def add_hook_to_embedding_layer(model, hook):
    embedding_layer = get_embedding_layer(model)
    embedding_layer.weight.requires_grad_(True)
    embedding_layer.register_backward_hook(hook)


def make_embeddings_lmo(embedding_layer):
    """Creates a function returning the Linear Maximization Oracle over 
    the polytope defined by the embedding vectors of the vocabulary."""
    embedding_matrix = embedding_layer.weight.detach().clone()

    @torch.no_grad()
    def lmo(grad, iterate):
        """Linear Maximization Oracle over the vocabulary polytope.
        Returns v - iterate, where v is the embedding of the word
        in the vocabulary which correlates the most with grad
        """
        update_direction = -iterate.clone().detach()
        gradient_dot_embedding_matrix = torch.einsum("bij,kj->bik",
                                                     (grad, embedding_matrix))
        _, best_words_ids = gradient_dot_embedding_matrix.max(2)
        best_embedding = torch.nn.functional.embedding(best_words_ids, embedding_matrix).detach()
        update_direction += best_embedding

        return update_direction, 1.

    return lmo


# %%
get_grad_hook = GetGradientHook()
embedding_layer = get_embedding_layer(model)
add_hook_to_embedding_layer(model, get_grad_hook)
lmo = make_embeddings_lmo(embedding_layer)

# %%
# Prepare dataset
dataset = load_dataset("amazon_reviews_multi")


def prepare(dataset):
    # Only use english reviews for now
    dataset = dataset.filter(lambda x: x['language'] == 'en', batched=True)
    # Rename stars column to labels
    dataset = dataset.map(lambda x: {'labels': x['stars']}, batched=True)
    # Tokenize here

    # Convert to PyTorch Tensors
    dataset.set_format(type='torch', columns=[
                       'input_ids', 'token_type_ids', 'attention_mask', 'labels'])
    return dataset


def prepend(tokenized_trigger, tokenized_sentence):

    for key in tokenized_sentence.keys():
        batch_size = tokenized_sentence[key].size(0)
        tokenized_sentence[key] = torch.cat((
            tokenized_trigger[key][..., :-1].repeat(batch_size, 1),
            tokenized_sentence[key][..., 1:]),
                                            -1)
    return tokenized_sentence




sentences = ["We are very happy to show you the 🤗 Transformers library.",
             "We hope you don't hate it."]

tok_options = {'padding': True, 'truncation': True,
               'max_length': 512, 'return_tensors': 'pt'}

trigger = " ".join(["the"] * 5)

tokenized_trigger = tokenizer(trigger, **tok_options)
data = tokenizer(sentences, **tok_options)
data_adv = tokenizer([" ".join((trigger, s)) for s in sentences], **tok_options)

target = torch.tensor([4, 0])

output = model(**data, labels=target)

loss = output.loss
loss.backward()

