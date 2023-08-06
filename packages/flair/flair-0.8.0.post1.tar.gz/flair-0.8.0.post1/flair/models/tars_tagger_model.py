from pathlib import Path
from typing import Union, Dict, List, Set, Optional

import torch
from torch.utils.data import Dataset

import flair

from flair.data import Dictionary, Sentence, Label
from flair.datasets import SentenceDataset, DataLoader
from flair.file_utils import cached_path
from flair.models import SequenceTagger

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import minmax_scale
import numpy as np

from tqdm import tqdm
import logging

from flair.training_utils import Result, store_embeddings, Metric

log = logging.getLogger("flair")


class TARSTagger(flair.nn.Model):
    """
    TARS Sequence Tagger Model
    The model inherits TextClassifier class to provide usual interfaces such as evaluate,
    predict etc. It can encapsulate multiple tasks inside it. The user has to mention
    which task is intended to be used. In the backend, the model uses a BERT based binary
    text classifier which given a <label, text> pair predicts the probability of two classes
    "YES", and "NO". The input data is a usual Sentence object which is inflated
    by the model internally before pushing it through the transformer stack of BERT.
    """

    static_label_type = "tars_label"
    static_adhoc_task_identifier = "adhoc_dummy"

    def __init__(
            self,
            task_name: str,
            tag_dictionary: Dictionary,
            tag_type: str,
            embeddings: str = 'bert-base-uncased',
            num_negative_labels_to_sample: int = 2,
            **tagger_args,
    ):
        """
        Initializes a TextClassifier
        :param task_name: a string depicting the name of the task
        :param label_dictionary: dictionary of labels you want to predict
        :param batch_size: batch size for forward pass while using BERT
        :param document_embeddings: name of the pre-trained transformer model e.g.,
        'bert-base-uncased' etc
        :num_negative_labels_to_sample: number of negative labels to sample for each
        positive labels against a sentence during training. Defaults to 2 negative
        labels for each positive label. The model would sample all the negative labels
        if None is passed. That slows down the training considerably.
        :param multi_label: auto-detected by default, but you can set this to True
        to force multi-label predictionor False to force single-label prediction
        :param multi_label_threshold: If multi-label you can set the threshold to make predictions
        :param beta: Parameter for F-beta score for evaluation and training annealing
        """

        super(TARSTagger, self).__init__()

        from flair.embeddings import TransformerWordEmbeddings

        if not isinstance(embeddings, TransformerWordEmbeddings):
            embeddings = TransformerWordEmbeddings(model=embeddings,
                                                   fine_tune=True,
                                                   layers='-1',
                                                   layer_mean=False,
                                                   )

        # prepare TARS dictionary
        tars_dictionary = Dictionary(add_unk=False)
        tars_dictionary.add_item('O')
        for tag in tag_dictionary.get_items():
            if "-" in tag:
                tars_dictionary.add_item(tag.split("-")[0] + '-')
        print('tars dictionary: ')
        print(tars_dictionary)

        self.tars_model = SequenceTagger(123,
                                         embeddings,
                                         tag_dictionary=tars_dictionary,
                                         tag_type=self.static_label_type,
                                         use_crf=False,
                                         use_rnn=False,
                                         reproject_embeddings=False,
                                         **tagger_args,
                                         )

        self.num_negative_labels_to_sample = num_negative_labels_to_sample
        self.label_nearest_map = None
        self.cleaned_up_labels = {}

        # Store task specific labels since TARS can handle multiple tasks
        self.current_task = None
        self.task_specific_attributes = {}
        self.add_and_switch_to_new_task(task_name, tag_dictionary, tag_type)

    def add_and_switch_to_new_task(self,
                                   task_name,
                                   label_dictionary: Union[List, Set, Dictionary, str],
                                   tag_type: str = None,
                                   ):
        """
        Adds a new task to an existing TARS model. Sets necessary attributes and finally 'switches'
        to the new task. Parameters are similar to the constructor except for model choice, batch
        size and negative sampling. This method does not store the resultant model onto disk.
        :param task_name: a string depicting the name of the task
        :param label_dictionary: dictionary of the labels you want to predict
        :param multi_label: auto-detect if a corpus label dictionary is provided. Defaults to True otherwise
        :param multi_label_threshold: If multi-label you can set the threshold to make predictions
        """
        if task_name in self.task_specific_attributes:
            log.warning("Task `%s` already exists in TARS model. Switching to it.", task_name)
        else:

            # make label dictionary if no Dictionary object is passed
            if isinstance(label_dictionary, (list, set, str)):
                label_dictionary = TARSTagger._make_ad_hoc_label_dictionary(label_dictionary)

            # prepare TARS dictionary
            tag_dictionary = Dictionary(add_unk=False)
            for tag in label_dictionary.get_items():
                if "-" in tag:
                    tag = tag.split("-")[1]
                    tag_dictionary.add_item(tag)
            print(tag_dictionary)

            self.task_specific_attributes[task_name] = {}
            self.task_specific_attributes[task_name]['tag_dictionary'] = tag_dictionary
            self.task_specific_attributes[task_name]['tag_type'] = tag_type

        self.switch_to_task(task_name)

    def list_existing_tasks(self) -> Set[str]:
        """
        Lists existing tasks in the loaded TARS model on the console.
        """
        return set(self.task_specific_attributes.keys())

    def _get_cleaned_up_label(self, label):
        """
        Does some basic clean up of the provided labels, stores them, looks them up.
        """
        if label not in self.cleaned_up_labels:
            self.cleaned_up_labels[label] = label.replace("_", " ")
        return self.cleaned_up_labels[label]

    def _compute_label_similarity_for_current_epoch(self):
        """
        Compute the similarity between all labels for better sampling of negatives
        """

        # get and embed all labels by making a Sentence object that contains only the label text
        all_labels = [label.decode("utf-8") for label in self.tag_dictionary.idx2item]
        label_sentences = [Sentence(self._get_cleaned_up_label(label)) for label in all_labels]
        self.tars_model.embeddings.embed(label_sentences)

        # get each label embedding and scale between 0 and 1
        encodings_np = [sentence[0].get_embedding().cpu().detach().numpy() for sentence in label_sentences]
        normalized_encoding = minmax_scale(encodings_np)

        # compute similarity matrix
        similarity_matrix = cosine_similarity(normalized_encoding)

        # the higher the similarity, the greater the chance that a label is
        # sampled as negative example
        negative_label_probabilities = {}
        for row_index, label in enumerate(all_labels):
            negative_label_probabilities[label] = {}
            for column_index, other_label in enumerate(all_labels):
                if label != other_label:
                    negative_label_probabilities[label][other_label] = \
                        similarity_matrix[row_index][column_index]
        self.label_nearest_map = negative_label_probabilities

    def train(self, mode=True):
        """Populate label similarity map based on cosine similarity before running epoch

        If the `num_negative_labels_to_sample` is set to an integer value then before starting
        each epoch the model would create a similarity measure between the label names based
        on cosine distances between their BERT encoded embeddings.
        """
        if mode and self.num_negative_labels_to_sample is not None:
            self._compute_label_similarity_for_current_epoch()
            super(TARSTagger, self).train(mode)

        super(TARSTagger, self).train(mode)

    def _get_nearest_labels_for(self, labels):

        if len(labels) == 0:
            tags = self.tag_dictionary.get_items()
            import random
            return random.sample(tags, k=self.num_negative_labels_to_sample)

        already_sampled_negative_labels = set()

        for label in labels:
            plausible_labels = []
            plausible_label_probabilities = []
            for plausible_label in self.label_nearest_map[label]:
                if plausible_label in already_sampled_negative_labels or plausible_label in labels:
                    continue
                else:
                    plausible_labels.append(plausible_label)
                    plausible_label_probabilities.append(self.label_nearest_map[label][plausible_label])

            # make sure the probabilities always sum up to 1
            plausible_label_probabilities = np.array(plausible_label_probabilities, dtype='float64')
            plausible_label_probabilities += 1e-08
            plausible_label_probabilities /= np.sum(plausible_label_probabilities)

            if len(plausible_labels) > 0:
                num_samples = min(self.num_negative_labels_to_sample, len(plausible_labels))
                sampled_negative_labels = np.random.choice(plausible_labels,
                                                           num_samples,
                                                           replace=False,
                                                           p=plausible_label_probabilities)
                already_sampled_negative_labels.update(sampled_negative_labels)

        return already_sampled_negative_labels

    def _get_tars_formatted_sentence(self, label, sentence):

        original_text = sentence.to_tokenized_string()

        label_text_pair = " ".join([
            original_text,
            self.tars_model.embeddings.tokenizer.sep_token,
            self._get_cleaned_up_label(label),],
        )

        tars_sentence = Sentence(label_text_pair, use_tokenizer=False)

        for token in sentence:
            tag = token.get_tag(self.tag_type).value
            tars_tag = tag.split('-')[0] + "-" if "-" in tag and tag.split('-')[1] == label else 'O'
            tars_sentence.get_token(token.idx).add_tag(self.static_label_type, tars_tag)

        return tars_sentence

    def _get_labels(self, sentence: Sentence) -> List[str]:
        labels = []
        for token in sentence:
            tag = token.get_tag(self.tag_type).value
            if "-" in tag:
                tag = tag.split('-')[1]
                if tag not in labels:
                    labels.append(tag)
        return labels

    def _get_tars_formatted_sentences(self, sentences):
        label_text_pairs = []
        all_labels = [label.decode("utf-8") for label in self.tag_dictionary.idx2item]
        # print(all_labels)
        for sentence in sentences:
            label_text_pairs_for_sentence = []
            if self.training and self.num_negative_labels_to_sample is not None:
                positive_labels = self._get_labels(sentence)
                # print(positive_labels)
                sampled_negative_labels = self._get_nearest_labels_for(positive_labels)
                # print(sampled_negative_labels)
                for label in positive_labels:
                    label_text_pairs_for_sentence.append(self._get_tars_formatted_sentence(label, sentence))
                for label in sampled_negative_labels:
                    label_text_pairs_for_sentence.append(self._get_tars_formatted_sentence(label, sentence))
            else:
                for label in all_labels:
                    label_text_pairs_for_sentence.append(self._get_tars_formatted_sentence(label, sentence))
            label_text_pairs.extend(label_text_pairs_for_sentence)
        return label_text_pairs

    def switch_to_task(self, task_name):
        """
        Switches to a task which was previously added.
        """
        if task_name not in self.task_specific_attributes:
            log.error("Provided `%s` does not exist in the model. Consider calling "
                      "`add_and_switch_to_new_task` first.", task_name)
        else:
            self.current_task = task_name
            self.tag_dictionary = self.task_specific_attributes[task_name]['tag_dictionary']
            self.tag_type = self.task_specific_attributes[task_name]['tag_type']

    def _get_state_dict(self):
        model_state = {
            "current_task": self.current_task,
            "task_specific_attributes": self.task_specific_attributes,
            "tars_model": self.tars_model,
            "num_negative_labels_to_sample": self.num_negative_labels_to_sample
        }
        return model_state

    @staticmethod
    def _init_model_with_state_dict(state):
        task_name = state["current_task"]
        print("init TARS")

        # init new TARS classifier
        model = TARSTagger(
            task_name,
            tag_dictionary=state["task_specific_attributes"][task_name]['label_dictionary'],
            tag_type=state["task_specific_attributes"][task_name]['tag_type'],
            document_embeddings=state["tars_model"].document_embeddings,
            num_negative_labels_to_sample=state["num_negative_labels_to_sample"],
        )
        # set all task information
        model.task_specific_attributes = state["task_specific_attributes"]
        # linear layers of internal classifier
        model.load_state_dict(state["state_dict"])
        return model

    def forward_loss(
            self, data_points: Union[List[Sentence], Sentence]
    ) -> torch.tensor:

        if type(data_points) == Sentence:
            data_points = [data_points]

        # Transform input data into TARS format
        sentences = self._get_tars_formatted_sentences(data_points)

        return self.tars_model.forward_loss(sentences)

    def _drop_task(self, task_name):
        if task_name in self.task_specific_attributes:
            if self.current_task == task_name:
                log.error("`%s` is the current task."
                          " Switch to some other task before dropping this.", task_name)
            else:
                self.task_specific_attributes.pop(task_name)
        else:
            log.warning("No task exists with the name `%s`.", task_name)

    @staticmethod
    def _filter_empty_sentences(sentences: List[Sentence]) -> List[Sentence]:
        filtered_sentences = [sentence for sentence in sentences if sentence.tokens]
        if len(sentences) != len(filtered_sentences):
            log.warning(
                f"Ignore {len(sentences) - len(filtered_sentences)} sentence(s) with no tokens."
            )
        return filtered_sentences

    @staticmethod
    def _fetch_model(model_name) -> str:

        model_map = {}
        hu_path: str = "https://nlp.informatik.hu-berlin.de/resources/models"

        model_map["tars-base"] = "/".join([hu_path, "tars-base", "tars-base-v8.pt"])

        cache_dir = Path("models")
        if model_name in model_map:
            model_name = cached_path(model_map[model_name], cache_dir=cache_dir)

        return model_name

    def evaluate(
            self,
            sentences: Union[List[Sentence], Dataset],
            out_path: Union[str, Path] = None,
            embedding_storage_mode: str = "none",
            mini_batch_size: int = 32,
            num_workers: int = 8,
            wsd_evaluation: bool = False
    ) -> (Result, float):

        # read Dataset into data loader (if list of sentences passed, make Dataset first)
        if not isinstance(sentences, Dataset):
            sentences = SentenceDataset(sentences)
        data_loader = DataLoader(sentences, batch_size=mini_batch_size, num_workers=num_workers)

        # if span F1 needs to be used, use separate eval method
        if self._requires_span_F1_evaluation() and not wsd_evaluation:
            return self._evaluate_with_span_F1(data_loader, embedding_storage_mode, mini_batch_size, out_path)

        # else, use scikit-learn to evaluate
        y_true = []
        y_pred = []
        labels = Dictionary(add_unk=False)

        eval_loss = 0
        batch_no: int = 0

        lines: List[str] = []

        for batch in data_loader:

            # predict for batch
            loss = self.predict(batch,
                                embedding_storage_mode=embedding_storage_mode,
                                mini_batch_size=mini_batch_size,
                                label_name='predicted',
                                return_loss=True)
            eval_loss += loss
            batch_no += 1

            for sentence in batch:

                for token in sentence:
                    # add gold tag
                    gold_tag = token.get_tag(self.tag_type).value
                    y_true.append(labels.add_item(gold_tag))

                    # add predicted tag
                    if wsd_evaluation:
                        if gold_tag == 'O':
                            predicted_tag = 'O'
                        else:
                            predicted_tag = token.get_tag('predicted').value
                    else:
                        predicted_tag = token.get_tag('predicted').value

                    y_pred.append(labels.add_item(predicted_tag))

                    # for file output
                    lines.append(f'{token.text} {gold_tag} {predicted_tag}\n')

                lines.append('\n')

        if out_path:
            with open(Path(out_path), "w", encoding="utf-8") as outfile:
                outfile.write("".join(lines))

        eval_loss /= batch_no

        # use sklearn
        from sklearn import metrics

        # make "classification report"
        target_names = []
        labels_to_report = []
        all_labels = []
        all_indices = []
        for i in range(len(labels)):
            label = labels.get_item_for_index(i)
            all_labels.append(label)
            all_indices.append(i)
            if label == '_' or label == '': continue
            target_names.append(label)
            labels_to_report.append(i)

        # report over all in case there are no labels
        if not labels_to_report:
            target_names = all_labels
            labels_to_report = all_indices

        classification_report = metrics.classification_report(y_true, y_pred, digits=4, target_names=target_names,
                                                              zero_division=1, labels=labels_to_report)

        # get scores
        micro_f_score = round(
            metrics.fbeta_score(y_true, y_pred, beta=self.tars_model.beta, average='micro', labels=labels_to_report), 4)
        macro_f_score = round(
            metrics.fbeta_score(y_true, y_pred, beta=self.tars_model.beta, average='macro', labels=labels_to_report), 4)
        accuracy_score = round(metrics.accuracy_score(y_true, y_pred), 4)

        detailed_result = (
                "\nResults:"
                f"\n- F-score (micro): {micro_f_score}"
                f"\n- F-score (macro): {macro_f_score}"
                f"\n- Accuracy (incl. no class): {accuracy_score}"
                '\n\nBy class:\n' + classification_report
        )

        # line for log file
        log_header = "ACCURACY"
        log_line = f"\t{accuracy_score}"

        result = Result(
            main_score=micro_f_score,
            log_line=log_line,
            log_header=log_header,
            detailed_results=detailed_result,
        )
        return result, eval_loss

    def _requires_span_F1_evaluation(self) -> bool:
        span_F1 = False
        for item in self.tag_dictionary.get_items():
            if item.startswith('B-'):
                span_F1 = True
        return span_F1

    def _evaluate_with_span_F1(self, data_loader, embedding_storage_mode, mini_batch_size, out_path):
        eval_loss = 0

        batch_no: int = 0

        metric = Metric("Evaluation", beta=self.beta)

        lines: List[str] = []

        y_true = []
        y_pred = []

        for batch in data_loader:

            # predict for batch
            loss = self.predict(batch,
                                embedding_storage_mode=embedding_storage_mode,
                                mini_batch_size=mini_batch_size,
                                label_name='predicted',
                                return_loss=True)
            eval_loss += loss
            batch_no += 1

            for sentence in batch:

                # make list of gold tags
                gold_spans = sentence.get_spans(self.tag_type)
                gold_tags = [(span.tag, repr(span)) for span in gold_spans]

                # make list of predicted tags
                predicted_spans = sentence.get_spans("predicted")
                predicted_tags = [(span.tag, repr(span)) for span in predicted_spans]

                # check for true positives, false positives and false negatives
                for tag, prediction in predicted_tags:
                    if (tag, prediction) in gold_tags:
                        metric.add_tp(tag)
                    else:
                        metric.add_fp(tag)

                for tag, gold in gold_tags:
                    if (tag, gold) not in predicted_tags:
                        metric.add_fn(tag)

                tags_gold = []
                tags_pred = []

                # also write to file in BIO format to use old conlleval script
                if out_path:
                    for token in sentence:
                        # check if in gold spans
                        gold_tag = 'O'
                        for span in gold_spans:
                            if token in span:
                                gold_tag = 'B-' + span.tag if token == span[0] else 'I-' + span.tag
                        tags_gold.append(gold_tag)

                        predicted_tag = 'O'
                        # check if in predicted spans
                        for span in predicted_spans:
                            if token in span:
                                predicted_tag = 'B-' + span.tag if token == span[0] else 'I-' + span.tag
                        tags_pred.append(predicted_tag)

                        lines.append(f'{token.text} {gold_tag} {predicted_tag}\n')
                    lines.append('\n')

                y_true.append(tags_gold)
                y_pred.append(tags_pred)

        if out_path:
            with open(Path(out_path), "w", encoding="utf-8") as outfile:
                outfile.write("".join(lines))

        eval_loss /= batch_no

        detailed_result = (
            "\nResults:"
            f"\n- F1-score (micro) {metric.micro_avg_f_score():.4f}"
            f"\n- F1-score (macro) {metric.macro_avg_f_score():.4f}"
            '\n\nBy class:'
        )

        for class_name in metric.get_classes():
            detailed_result += (
                f"\n{class_name:<10} tp: {metric.get_tp(class_name)} - fp: {metric.get_fp(class_name)} - "
                f"fn: {metric.get_fn(class_name)} - precision: "
                f"{metric.precision(class_name):.4f} - recall: {metric.recall(class_name):.4f} - "
                f"f1-score: "
                f"{metric.f_score(class_name):.4f}"
            )

        result = Result(
            main_score=metric.micro_avg_f_score(),
            log_line=f"{metric.precision():.4f}\t{metric.recall():.4f}\t{metric.micro_avg_f_score():.4f}",
            log_header="PRECISION\tRECALL\tF1",
            detailed_results=detailed_result,
        )

        return result, eval_loss

    def predict(
            self,
            sentences: Union[List[Sentence], Sentence],
            mini_batch_size=32,
            all_tag_prob: bool = False,
            verbose: bool = False,
            label_name: Optional[str] = None,
            return_loss=False,
            embedding_storage_mode="none",
    ):
        """
        Predict sequence tags for Named Entity Recognition task
        :param sentences: a Sentence or a List of Sentence
        :param mini_batch_size: size of the minibatch, usually bigger is more rapid but consume more memory,
        up to a point when it has no more effect.
        :param all_tag_prob: True to compute the score for each tag on each token,
        otherwise only the score of the best tag is returned
        :param verbose: set to True to display a progress bar
        :param return_loss: set to True to return loss
        :param label_name: set this to change the name of the label type that is predicted
        :param embedding_storage_mode: default is 'none' which is always best. Only set to 'cpu' or 'gpu' if
        you wish to not only predict, but also keep the generated embeddings in CPU or GPU memory respectively.
        'gpu' to store embeddings in GPU memory.
        """
        if label_name == None:
            label_name = self.tag_type

        with torch.no_grad():
            if not sentences:
                return sentences

            if isinstance(sentences, Sentence):
                sentences = [sentences]

            # set context if not set already
            previous_sentence = None
            for sentence in sentences:
                if sentence.is_context_set(): continue
                sentence._previous_sentence = previous_sentence
                sentence._next_sentence = None
                if previous_sentence: previous_sentence._next_sentence = sentence
                previous_sentence = sentence

            # reverse sort all sequences by their length
            rev_order_len_index = sorted(
                range(len(sentences)), key=lambda k: len(sentences[k]), reverse=True
            )

            reordered_sentences: List[Union[Sentence, str]] = [
                sentences[index] for index in rev_order_len_index
            ]

            dataloader = DataLoader(
                dataset=SentenceDataset(reordered_sentences), batch_size=mini_batch_size
            )

            # progress bar for verbosity
            if verbose:
                dataloader = tqdm(dataloader)

            overall_loss = torch.tensor(0)
            batch_no = 0
            for batch in dataloader:

                batch_no += 1

                if verbose:
                    dataloader.set_description(f"Inferencing on batch {batch_no}")

                batch = self._filter_empty_sentences(batch)
                # stop if all sentences are empty
                if not batch:
                    continue

                # print(self.tag_dictionary)

                for sentence in batch:
                    all_labels = [label.decode("utf-8") for label in self.tag_dictionary.idx2item]

                    # confidence_label_map = {}

                    for label in all_labels:
                        tars_sentence = self._get_tars_formatted_sentence(label, sentence)
                        self.tars_model.predict(tars_sentence, label_name=label_name, all_tag_prob=True)

                        for span in tars_sentence.get_spans(label_name):
                            for token in span:
                                sentence.get_token(token.idx).add_tag(
                                    label_name,
                                    token.get_tag(label_name).value + label,
                                    token.get_tag(label_name).score,
                                )
                        # print(tars_sentence.get_spans(label_name))
                        # print(tars_sentence)
                        # for token in tars_sentence:
                        #     print(token.tags_proba_dist[label_name])

                # print(sentence.to_tagged_string(label_name))
                # formatted_sentences = self._get_tars_formatted_sentences(batch)

                # for sentence in formatted_sentences:
                #     print(sentence.to_tagged_string(label_name))

                # print(formatted_sentences)
                # asd

                # for tag in self.tag_dictionary.get_items():
                #
                #
                #     self.tars_model.predict()
                # asd

                #
                # if return_loss:
                #     overall_loss += self._calculate_loss(feature, batch)

                # tags, all_tags = self._obtain_labels(
                #     feature=feature,
                #     batch_sentences=batch,
                #     transitions=transitions,
                #     get_all_tags=all_tag_prob,
                # )

                # for (sentence, sent_tags) in zip(batch, tags):
                #     for (token, tag) in zip(sentence.tokens, sent_tags):
                #         token.add_tag_label(label_name, tag)
                #
                # # all_tags will be empty if all_tag_prob is set to False, so the for loop will be avoided
                # for (sentence, sent_all_tags) in zip(batch, all_tags):
                #     for (token, token_all_tags) in zip(sentence.tokens, sent_all_tags):
                #         token.add_tags_proba_dist(label_name, token_all_tags)

                # clearing token embeddings to save memory
                store_embeddings(batch, storage_mode=embedding_storage_mode)

            if return_loss:
                return overall_loss / batch_no
