from typing import List
from loguru import logger
from math import ceil

from rich.progress import track

from sklearn.metrics import ndcg_score
import numpy as np

from sadedegel.config import tokenizer_context
from sadedegel.summarize import BandSummarizer, RandomSummarizer
from sadedegel.dataset import load_annotated_corpus

logger.disable("sadedegel")

import wandb


# wandb.login()


def evaluate_summarizer(summarizer, relevance, doc_sg):
    score_10, score_50, score_80 = [], [], []

    for i, (y_true, d) in enumerate(zip(relevance, doc_sg)):
        y_pred = [summarizer.predict([s for s in d])]

        score_10.append(ndcg_score(y_true, y_pred, k=ceil(len(d) * 0.1)))
        score_50.append(ndcg_score(y_true, y_pred, k=ceil(len(d) * 0.5)))
        score_80.append(ndcg_score(y_true, y_pred, k=ceil(len(d) * 0.8)))

    return np.array(score_10).mean(), np.array(score_50).mean(), np.array(score_80).mean()


def run_rand(docs):
    wandb.init(project='sadedegel')

    from sadedegel import Doc
    config = wandb.config
    config.method = "rand"

    relevance = [[doc['relevance']] for doc in docs]

    doc_sg = [Doc.from_sentences(doc['sentences']) for doc in track(docs)]

    summarizer = RandomSummarizer()

    score_10, score_50, score_80 = evaluate_summarizer(summarizer, relevance, doc_sg)

    wandb.log(dict(score_10=score_10, score_50=score_50,
                   score_80=score_50))


def run_band(docs, tokenizers: List[int], k_list: List[int]):
    wandb.init(project='sadedegel')

    config = wandb.config
    config.method = "band"

    relevance = [[doc['relevance']] for doc in docs]

    for tokenizer in tokenizers:
        config.tokenizer = tokenizer

        with tokenizer_context(tokenizer) as Doc:

            doc_sg = [Doc.from_sentences(doc['sentences']) for doc in track(docs)]

            for k in k_list:
                config.k = k
                summarizer = BandSummarizer(k)

                score_10, score_50, score_80 = evaluate_summarizer(summarizer, relevance, doc_sg)

                wandb.log(dict(score_10=score_10, score_50=score_50,
                               score_80=score_50))


if __name__ == '__main__':
    anno = load_annotated_corpus(False)

    run_band(anno, tokenizers=['simple', 'bert'], k_list=[2, 3, 6, 8])
    run_rand(anno)
