import pytest

from auto_labeling_pipeline.labels import ClassificationLabels, Seq2seqLabels, SequenceLabels


@pytest.fixture
def example_classification_data():
    labels = [
        {'label': 'A'},
        {'label': 'B'},
        {'label': 'C'}
    ]
    labels = ClassificationLabels(labels)
    return labels


@pytest.fixture
def example_sequence_data():
    labels = [
        {'label': 'A', 'start_offset': 0, 'end_offset': 1},
        {'label': 'B', 'start_offset': 1, 'end_offset': 2},
        {'label': 'C', 'start_offset': 2, 'end_offset': 3}
    ]
    labels = SequenceLabels(labels)
    return labels


@pytest.fixture
def example_seq2seq_data():
    labels = [
        {'text': 'A'},
        {'text': 'B'},
        {'text': 'C'}
    ]
    labels = Seq2seqLabels(labels)
    return labels


@pytest.fixture
def example_sequence_overlap_data():
    labels = [
        {'label': 'A', 'start_offset': 0, 'end_offset': 2},
        {'label': 'B', 'start_offset': 1, 'end_offset': 2}
    ]
    labels = SequenceLabels(labels)
    return labels


class TestClassificationLabels:

    def test_filter_by_name(self, example_classification_data):
        vocabulary = {'A'}
        labels = example_classification_data.filter_by_name(vocabulary)
        labels = labels.dict()
        expected = [
            {'label': 'A'}
        ]
        assert labels == expected

    def test_dont_filter_by_name(self, example_classification_data):
        labels = example_classification_data.filter_by_name()
        assert labels == example_classification_data

    def test_convert_label(self, example_classification_data):
        mapping = {'C': 'D'}
        labels = example_classification_data.replace_label(mapping)
        labels = labels.dict()
        expected = [
            {'label': 'A'},
            {'label': 'B'},
            {'label': 'D'}
        ]
        assert labels == expected

    def test_dont_convert_label(self, example_classification_data):
        labels = example_classification_data.replace_label()
        assert labels == example_classification_data

    def test_merge(self):
        labels = ClassificationLabels([{'label': 'A'}, {'label': 'C'}])
        other = ClassificationLabels([{'label': 'A'}, {'label': 'B'}])
        labels = labels.merge(other)
        expected = [{'label': 'A'}, {'label': 'B'}, {'label': 'C'}]
        actual = sorted(labels.dict(), key=lambda x: x['label'])
        assert actual == expected


class TestSequenceLabels:

    def test_filter_by_name(self, example_sequence_data):
        vocabulary = {'A'}
        labels = example_sequence_data.filter_by_name(vocabulary)
        labels = labels.dict()
        expected = [
            {'label': 'A', 'start_offset': 0, 'end_offset': 1}
        ]
        assert labels == expected

    def test_dont_filter_by_name(self, example_sequence_data):
        labels = example_sequence_data.filter_by_name()
        assert labels == example_sequence_data

    def test_convert_label(self, example_sequence_data):
        mapping = {'C': 'D'}
        labels = example_sequence_data.replace_label(mapping)
        labels = labels.dict()
        expected = [
            {'label': 'A', 'start_offset': 0, 'end_offset': 1},
            {'label': 'B', 'start_offset': 1, 'end_offset': 2},
            {'label': 'D', 'start_offset': 2, 'end_offset': 3}
        ]
        assert labels == expected

    def test_dont_convert_label(self, example_sequence_data):
        labels = example_sequence_data.replace_label()
        assert labels == example_sequence_data

    def test_remove_overlap(self, example_sequence_overlap_data):
        labels = example_sequence_overlap_data.remove_overlapping()
        assert len(labels.dict()) == 1

    def test_merge(self):
        labels = SequenceLabels([
            {'label': 'A', 'start_offset': 0, 'end_offset': 1},
            {'label': 'B', 'start_offset': 3, 'end_offset': 5}
        ])
        others = SequenceLabels([
            {'label': 'C', 'start_offset': 1, 'end_offset': 3},
            {'label': 'B', 'start_offset': 1, 'end_offset': 2}
        ])
        labels = labels.merge(others)
        expected = [
            {'label': 'A', 'start_offset': 0, 'end_offset': 1},
            {'label': 'C', 'start_offset': 1, 'end_offset': 3},
            {'label': 'B', 'start_offset': 3, 'end_offset': 5}
        ]
        actual = sorted(labels.dict(), key=lambda x: x['start_offset'])
        assert actual == expected


class TestSeq2seqLabels:

    def test_filter_by_name(self, example_seq2seq_data):
        stop_labels = {'B', 'C', 'D'}
        labels = example_seq2seq_data.filter_by_name(stop_labels)
        assert labels == example_seq2seq_data

    def test_convert_label(self, example_seq2seq_data):
        mapping = {'C': 'D'}
        labels = example_seq2seq_data.replace_label(mapping)
        assert labels == example_seq2seq_data

    def test_merge(self):
        labels = Seq2seqLabels([{'text': 'A'}, {'text': 'C'}])
        other = Seq2seqLabels([{'text': 'A'}, {'text': 'B'}])
        labels = labels.merge(other)
        expected = [{'text': 'A'}, {'text': 'B'}, {'text': 'C'}]
        actual = sorted(labels.dict(), key=lambda x: x['text'])
        assert actual == expected
