import pickle

import tensorflow as tf

from common import WORDS_FEATURE, tic, toc, create_parser_training, parse_arguments, \
    preprocess_data, run_experiment, estimator_spec_for_softmax_classification

MODEL_DIRECTORY = 'perceptron_model'
#SPLIT_SEED = 1234
NUM_EPOCHS = 2
BATCH_SIZE = 64
LEARNING_RATE = 0.005


def bag_of_words_perceptron(features, labels, mode, params):
    """Perceptron architecture"""
    with tf.variable_scope('Perceptron'):
        bow_column = tf.feature_column.categorical_column_with_identity(
            WORDS_FEATURE, num_buckets=params.n_words)
        # By default embeding_column combines the word embedding values by taking the mean value
        # of the embedding values over the document words. Try weighted sum, via sqrtn?
        bow_embedding_column = tf.feature_column.embedding_column(
            bow_column, dimension=params.output_dim)
        logits = tf.feature_column.input_layer(
            features,
            feature_columns=[bow_embedding_column])

    return estimator_spec_for_softmax_classification(logits, labels, mode, params)


def perceptron(unused_argv):
    """Trains the perceptron model."""
    tf.logging.set_verbosity(FLAGS.verbosity)

    print("Preprocessing data...")
    tic()
    train_raw, x_train, y_train, x_test, y_test, classes = preprocess_data(FLAGS)
    toc()

    # Set the output dimension according to the number of classes
    FLAGS.output_dim = len(classes)

    # Train the model.
    tic()
    run_experiment(x_train, y_train, x_test, y_test, bag_of_words_perceptron, 'train_and_evaluate', FLAGS)
    toc()


# Run script ##############################################
if __name__ == "__main__":
    # Get common parser
    parser = create_parser_training(MODEL_DIRECTORY, NUM_EPOCHS, BATCH_SIZE, LEARNING_RATE)

    FLAGS = parse_arguments(parser)

    tf.app.run(perceptron)
