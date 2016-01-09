"""
Configuration options for running Spark performance tests.

When updating `spark-perf`, you should probably use `diff` to compare the updated template to
your modified `config.py` file and copy over any new configurations.
"""

import time
import os
import os.path
import socket

from sparkperf.config_utils import FlagSet, JavaOptionSet, OptionSet, ConstantOption


# ================================ #
#  Standard Configuration Options  #
# ================================ #

# Point to an installation of Spark on the cluster.
SPARK_HOME_DIR = "/mnt/yggdrasil"

# Use a custom configuration directory
SPARK_CONF_DIR = SPARK_HOME_DIR + "/conf"

# Master used when submitting Spark jobs.
# For local clusters: "spark://%s:7077" % socket.gethostname()
# For Yarn clusters: "yarn"
# Otherwise, the default uses the specified EC2 cluster
SPARK_CLUSTER_URL = open("/root/spark-ec2/cluster-url", 'r').readline().strip()
IS_YARN_MODE = "yarn" in SPARK_CLUSTER_URL
IS_MESOS_MODE = "mesos" in SPARK_CLUSTER_URL

# Specify URI to download spark executor. This only applied for running with Mesos.
#SPARK_EXECUTOR_URI = "http://localhost:8000/spark.tgz"

# Path to the Mesos native library. This is only required for running with Mesos.
#MESOS_NATIVE_LIBRARY = "/usr/local/lib/libmesos.so"

# Run Mesos client in coarse or fine grain mode. This is only applied for running with Mesos.
#SPARK_MESOS_COARSE = True


# If this is true, we'll submit your job using an existing Spark installation.
# If this is false, we'll clone and build a specific version of Spark, and
# copy configurations from your existing Spark installation.
USE_CLUSTER_SPARK = True

# URL of the HDFS installation in the Spark EC2 cluster
HDFS_URL = "hdfs://%s:9000/test/" % socket.gethostname()

# Set the following if not using existing Spark installation
# Commit id and repo used if you are not using an existing Spark cluster
# custom version of Spark. The remote name in your git repo is assumed
# to be "origin".
#
# The commit ID can specify any of the following:
#     1. A git commit hash         e.g. "4af93ff3"
#     2. A branch name             e.g. "origin/branch-0.7"
#     3. A tag name                e.g. "origin/tag/v0.8.0-incubating"
#     4. A pull request            e.g. "origin/pr/675"
SPARK_COMMIT_ID = ""
SPARK_GIT_REPO = "https://github.com/apache/spark.git"
SPARK_MERGE_COMMIT_INTO_MASTER = False # Whether to merge the commit into master

# Whether to install and build Spark. Set this to true only for the
# first installation if an existing one does not already exist.
PREP_SPARK = not USE_CLUSTER_SPARK

# Whether to restart the Master and all Workers
# This should always be false for Yarn
RESTART_SPARK_CLUSTER = True
RESTART_SPARK_CLUSTER = RESTART_SPARK_CLUSTER and not IS_YARN_MODE

# Rsync SPARK_HOME to all the slaves or not
RSYNC_SPARK_HOME = True

# Which tests to run
RUN_SPARK_TESTS = False
RUN_PYSPARK_TESTS = False
RUN_STREAMING_TESTS = False
RUN_MLLIB_TESTS = True
RUN_PYTHON_MLLIB_TESTS = False

# Which tests to prepare. Set this to true for the first
# installation or whenever you make a change to the tests.
PREP_SPARK_TESTS = False
PREP_PYSPARK_TESTS = False
PREP_STREAMING_TESTS = False
PREP_MLLIB_TESTS = False

# Whether to warm up local disks (warm-up is only necesary on EC2).
DISK_WARMUP = True

# Total number of bytes used to warm up each local directory.
DISK_WARMUP_BYTES = 200 * 1024 * 1024

# Number of files to create when warming up each local directory.
# Bytes will be evenly divided across files.
DISK_WARMUP_FILES = 200

# Prompt for confirmation when deleting temporary files.
PROMPT_FOR_DELETES = True

# Files to write results to
SPARK_OUTPUT_FILENAME = "results/spark_perf_output_%s_%s" % (
    SPARK_COMMIT_ID.replace("/", "-"), time.strftime("%Y-%m-%d_%H-%M-%S"))
PYSPARK_OUTPUT_FILENAME = "results/python_perf_output_%s_%s" % (
    SPARK_COMMIT_ID.replace("/", "-"), time.strftime("%Y-%m-%d_%H-%M-%S"))
STREAMING_OUTPUT_FILENAME = "results/streaming_perf_output_%s_%s" % (
    SPARK_COMMIT_ID.replace("/", "-"), time.strftime("%Y-%m-%d_%H-%M-%S"))
MLLIB_OUTPUT_FILENAME = "results/mllib_perf_output_%s_%s" % (
    SPARK_COMMIT_ID.replace("/", "-"), time.strftime("%Y-%m-%d_%H-%M-%S"))
PYTHON_MLLIB_OUTPUT_FILENAME = "results/python_mllib_perf_output_%s_%s" % (
    SPARK_COMMIT_ID.replace("/", "-"), time.strftime("%Y-%m-%d_%H-%M-%S"))


# ============================ #
#  Test Configuration Options  #
# ============================ #

# The default values configured below are appropriate for approximately 20 m1.xlarge nodes,
# in which each node has 15 GB of memory. Use this variable to scale the values (e.g.
# number of records in a generated dataset) if you are running the tests with more
# or fewer nodes. When developing new test suites, you might want to set this to a small
# value suitable for a single machine, such as 0.001.
SCALE_FACTOR = 1.0

assert SCALE_FACTOR > 0, "SCALE_FACTOR must be > 0."

# If set, removes the first N trials for each test from all reported statistics. Useful for
# tests which have outlier behavior due to JIT and other system cache warm-ups. If any test
# returns fewer N + 1 results, an exception is thrown.
IGNORED_TRIALS = 2

# Command used to launch Scala or Java.

# Set up OptionSets. Note that giant cross product is done over all JavaOptionsSets + OptionSets
# passed to each test which may be combinations of those set up here.

# Java options.
COMMON_JAVA_OPTS = [
    # Fraction of JVM memory used for caching RDDs.
    JavaOptionSet("spark.storage.memoryFraction", [0.66]),
    JavaOptionSet("spark.serializer", ["org.apache.spark.serializer.JavaSerializer"]),
    # JavaOptionSet("spark.executor.memory", ["9g"]),
    # Turn event logging on in order better diagnose failed tests. Off by default as it crashes
    # releases prior to 1.0.2
    # JavaOptionSet("spark.eventLog.enabled", [True]),
    # To ensure consistency across runs, we disable delay scheduling
    JavaOptionSet("spark.locality.wait", [str(60 * 1000 * 1000)])
]
# Set driver memory here
SPARK_DRIVER_MEMORY = "20g"
# The following options value sets are shared among all tests.
COMMON_OPTS = [
    # How many times to run each experiment - used to warm up system caches.
    # This OptionSet should probably only have a single value (i.e., length 1)
    # since it doesn't make sense to have multiple values here.
    OptionSet("num-trials", [2]),
    # Extra pause added between trials, in seconds. For runs with large amounts
    # of shuffle data, this gives time for buffer cache write-back.
    OptionSet("inter-trial-wait", [3])
]

# The following options value sets are shared among all tests of
# operations on key-value data.
SPARK_KEY_VAL_TEST_OPTS = [
    # The number of input partitions.
    OptionSet("num-partitions", [400], can_scale=True),
    # The number of reduce tasks.
    OptionSet("reduce-tasks", [400], can_scale=True),
    # A random seed to make tests reproducable.
    OptionSet("random-seed", [5]),
    # Input persistence strategy (can be "memory", "disk", or "hdfs").
    # NOTE: If "hdfs" is selected, datasets will be re-used across runs of
    #       this script. This means parameters here are effectively ignored if
    #       an existing input dataset is present.
    OptionSet("persistent-type", ["memory"]),
    # Whether to wait for input in order to exit the JVM.
    FlagSet("wait-for-exit", [False]),
    # Total number of records to create.
    OptionSet("num-records", [200 * 1000 * 1000], True),
    # Number of unique keys to sample from.
    OptionSet("unique-keys",[20 * 1000], True),
    # Length in characters of each key.
    OptionSet("key-length", [10]),
    # Number of unique values to sample from.
    OptionSet("unique-values", [1000 * 1000], True),
    # Length in characters of each value.
    OptionSet("value-length", [10]),
    # Use hashes instead of padded numbers for keys and values
    FlagSet("hash-records", [False]),
    # Storage location if HDFS persistence is used
    OptionSet("storage-location", [
        HDFS_URL + "/spark-perf-kv-data"])
]


# ======================= #
#  Spark Core Test Setup  #
# ======================= #

# Set up the actual tests. Each test is represtented by a tuple:
# (short_name, test_cmd, scale_factor, list<JavaOptionSet>, list<OptionSet>)

SPARK_KV_OPTS = COMMON_OPTS + SPARK_KEY_VAL_TEST_OPTS
SPARK_TESTS = []

SCHEDULING_THROUGHPUT_OPTS = [
    # The number of tasks that should be launched in each job:
    OptionSet("num-tasks", [10 * 1000]),
    # The number of jobs that should be run:
    OptionSet("num-jobs", [1]),
    # The size of the task closure (in bytes):
    OptionSet("closure-size", [0]),
    # A random seed to make tests reproducible:
    OptionSet("random-seed", [5]),
]

SPARK_TESTS += [("scheduling-throughput", "spark.perf.TestRunner",
    SCALE_FACTOR, COMMON_JAVA_OPTS,
    [ConstantOption("scheduling-throughput")] + COMMON_OPTS + SCHEDULING_THROUGHPUT_OPTS)]

SPARK_TESTS += [("scala-agg-by-key", "spark.perf.TestRunner", SCALE_FACTOR,
    COMMON_JAVA_OPTS, [ConstantOption("aggregate-by-key")] + SPARK_KV_OPTS)]

# Scale the input for this test by 2x since ints are smaller.
SPARK_TESTS += [("scala-agg-by-key-int", "spark.perf.TestRunner", SCALE_FACTOR * 2,
    COMMON_JAVA_OPTS, [ConstantOption("aggregate-by-key-int")] + SPARK_KV_OPTS)]

SPARK_TESTS += [("scala-agg-by-key-naive", "spark.perf.TestRunner", SCALE_FACTOR,
    COMMON_JAVA_OPTS, [ConstantOption("aggregate-by-key-naive")] + SPARK_KV_OPTS)]

# Scale the input for this test by 0.10.
SPARK_TESTS += [("scala-sort-by-key", "spark.perf.TestRunner", SCALE_FACTOR * 0.1,
    COMMON_JAVA_OPTS, [ConstantOption("sort-by-key")] + SPARK_KV_OPTS)]

SPARK_TESTS += [("scala-sort-by-key-int", "spark.perf.TestRunner", SCALE_FACTOR * 0.2,
    COMMON_JAVA_OPTS, [ConstantOption("sort-by-key-int")] + SPARK_KV_OPTS)]

SPARK_TESTS += [("scala-count", "spark.perf.TestRunner", SCALE_FACTOR,
    COMMON_JAVA_OPTS, [ConstantOption("count")] + SPARK_KV_OPTS)]

SPARK_TESTS += [("scala-count-w-fltr", "spark.perf.TestRunner", SCALE_FACTOR,
    COMMON_JAVA_OPTS, [ConstantOption("count-with-filter")] + SPARK_KV_OPTS)]


# ==================== #
#  Pyspark Test Setup  #
# ==================== #

PYSPARK_TESTS = []

BROADCAST_TEST_OPTS = [
    # The size of broadcast
    OptionSet("broadcast-size", [200 << 20], can_scale=True),
]

PYSPARK_TESTS += [("python-scheduling-throughput", "core_tests.py",
    SCALE_FACTOR, COMMON_JAVA_OPTS,
    [ConstantOption("SchedulerThroughputTest"), OptionSet("num-tasks", [5000])] + COMMON_OPTS)]

PYSPARK_TESTS += [("python-agg-by-key", "core_tests.py", SCALE_FACTOR,
    COMMON_JAVA_OPTS, [ConstantOption("AggregateByKey")] + SPARK_KV_OPTS)]

# Scale the input for this test by 2x since ints are smaller.
PYSPARK_TESTS += [("python-agg-by-key-int", "core_tests.py", SCALE_FACTOR * 2,
    COMMON_JAVA_OPTS, [ConstantOption("AggregateByKeyInt")] + SPARK_KV_OPTS)]

PYSPARK_TESTS += [("python-agg-by-key-naive", "core_tests.py", SCALE_FACTOR,
    COMMON_JAVA_OPTS, [ConstantOption("AggregateByKeyNaive")] + SPARK_KV_OPTS)]

# Scale the input for this test by 0.10.
PYSPARK_TESTS += [("python-sort-by-key", "core_tests.py", SCALE_FACTOR * 0.1,
    COMMON_JAVA_OPTS, [ConstantOption("SortByKey")] + SPARK_KV_OPTS)]

PYSPARK_TESTS += [("python-sort-by-key-int", "core_tests.py", SCALE_FACTOR * 0.2,
    COMMON_JAVA_OPTS, [ConstantOption("SortByKeyInt")] + SPARK_KV_OPTS)]

PYSPARK_TESTS += [("python-count", "core_tests.py", SCALE_FACTOR,
                 COMMON_JAVA_OPTS, [ConstantOption("Count")] + SPARK_KV_OPTS)]

PYSPARK_TESTS += [("python-count-w-fltr", "core_tests.py", SCALE_FACTOR,
    COMMON_JAVA_OPTS, [ConstantOption("CountWithFilter")] + SPARK_KV_OPTS)]

PYSPARK_TESTS += [("python-broadcast-w-bytes", "core_tests.py", SCALE_FACTOR,
    COMMON_JAVA_OPTS, [ConstantOption("BroadcastWithBytes")] + SPARK_KV_OPTS + BROADCAST_TEST_OPTS)]

PYSPARK_TESTS += [("python-broadcast-w-set", "core_tests.py", SCALE_FACTOR,
    COMMON_JAVA_OPTS, [ConstantOption("BroadcastWithSet")] + SPARK_KV_OPTS + BROADCAST_TEST_OPTS)]


# ============================ #
#  Spark Streaming Test Setup  #
# ============================ #

STREAMING_TESTS = []

# The following function generates options for setting batch duration in streaming tests
def streaming_batch_duration_opts(duration):
    return [OptionSet("batch-duration", [duration])]

# The following function generates options for setting window duration in streaming tests
def streaming_window_duration_opts(duration):
    return [OptionSet("window-duration", [duration])]

STREAMING_COMMON_OPTS = [
    OptionSet("total-duration", [60]),
    OptionSet("hdfs-url", [HDFS_URL]),
]

STREAMING_COMMON_JAVA_OPTS = [
    # Fraction of JVM memory used for caching RDDs.
    JavaOptionSet("spark.storage.memoryFraction", [0.66]),
    JavaOptionSet("spark.serializer", ["org.apache.spark.serializer.JavaSerializer"]),
    # JavaOptionSet("spark.executor.memory", ["9g"]),
    JavaOptionSet("spark.executor.extraJavaOptions", [" -XX:+UseConcMarkSweepGC "])
]

STREAMING_KEY_VAL_TEST_OPTS = STREAMING_COMMON_OPTS + streaming_batch_duration_opts(2000) + [
    # Number of input streams.
    OptionSet("num-streams", [1], can_scale=True),
    # Number of records per second per input stream
    OptionSet("records-per-sec", [10 * 1000]),
    # Number of reduce tasks.
    OptionSet("reduce-tasks", [10], can_scale=True),
    # memory serialization ("true" or "false").
    OptionSet("memory-serialization", ["true"]),
    # Number of unique keys to sample from.
    OptionSet("unique-keys",[100 * 1000], can_scale=True),
    # Length in characters of each key.
    OptionSet("unique-values", [1000 * 1000], can_scale=True),
    # Send data through receiver
    OptionSet("use-receiver", ["true"]),
]

STREAMING_HDFS_RECOVERY_TEST_OPTS = STREAMING_COMMON_OPTS + streaming_batch_duration_opts(5000) + [
    OptionSet("records-per-file", [10000]),
    OptionSet("file-cleaner-delay", [300])
]

# This test is just to see if everything is setup properly
STREAMING_TESTS += [("basic", "streaming.perf.TestRunner", SCALE_FACTOR,
    STREAMING_COMMON_JAVA_OPTS, [ConstantOption("basic")] + STREAMING_COMMON_OPTS + streaming_batch_duration_opts(1000))]

STREAMING_TESTS += [("state-by-key", "streaming.perf.TestRunner", SCALE_FACTOR,
    STREAMING_COMMON_JAVA_OPTS, [ConstantOption("state-by-key")] + STREAMING_KEY_VAL_TEST_OPTS)]

STREAMING_TESTS += [("group-by-key-and-window", "streaming.perf.TestRunner", SCALE_FACTOR,
    STREAMING_COMMON_JAVA_OPTS, [ConstantOption("group-by-key-and-window")] + STREAMING_KEY_VAL_TEST_OPTS + streaming_window_duration_opts(10000) )]

STREAMING_TESTS += [("reduce-by-key-and-window", "streaming.perf.TestRunner", SCALE_FACTOR,
    STREAMING_COMMON_JAVA_OPTS, [ConstantOption("reduce-by-key-and-window")] + STREAMING_KEY_VAL_TEST_OPTS + streaming_window_duration_opts(10000) )]

STREAMING_TESTS += [("hdfs-recovery", "streaming.perf.TestRunner", SCALE_FACTOR,
    STREAMING_COMMON_JAVA_OPTS, [ConstantOption("hdfs-recovery")] + STREAMING_HDFS_RECOVERY_TEST_OPTS)]


# ================== #
#  MLlib Test Setup  #
# ================== #

MLLIB_TESTS = []
MLLIB_PERF_TEST_RUNNER = "mllib.perf.TestRunner"

# Set this to 1.0, 1.1, 1.2, ... (the major version) to test MLlib with a particular Spark version.
# Note: You should also build mllib-perf using -Dspark.version to specify the same version.
# Note: To run perf tests against a snapshot version of Spark which has not yet been packaged into a release:
#  * Build Spark locally by running `build/sbt assembly; build/sbt publishLocal` in the Spark root directory
#  * Set `USE_CLUSTER_SPARK = True` and `MLLIB_SPARK_VERSION = {desired Spark version, e.g. 1.5}`
#  * Don't use PREP_MLLIB_TESTS = True; instead manually run `cd mllib-tests; sbt/sbt -Dspark.version=1.5.0-SNAPSHOT clean assembly` to build perf tests
MLLIB_SPARK_VERSION = 1.5

MLLIB_JAVA_OPTS = COMMON_JAVA_OPTS
if MLLIB_SPARK_VERSION >= 1.1:
    MLLIB_JAVA_OPTS = MLLIB_JAVA_OPTS + [
        # Shuffle manager: SORT, HASH
        JavaOptionSet("spark.shuffle.manager", ["SORT"])
    ]

# The following options value sets are shared among all tests of
# operations on MLlib algorithms.
MLLIB_COMMON_OPTS = COMMON_OPTS + [
    # The number of input partitions.
    # The default setting is suitable for a 16-node m3.2xlarge EC2 cluster.
    OptionSet("num-partitions", [128], can_scale=True),
    # A random seed to make tests reproducable.
    OptionSet("random-seed", [5])
]

# Decision Trees #
MLLIB_DECISION_TREE_TEST_OPTS = MLLIB_COMMON_OPTS + [
    # The number of rows or examples
    OptionSet("num-examples", [1000000, 1500000, 2000000], can_scale=True),
    # The number of features per example
    OptionSet("num-features", [500, 1000, 1500, 2000], can_scale=False),
    # Type of label: 0 indicates regression, 2+ indicates classification with this many classes
    # Note: multi-class (>2) is not supported in Spark 1.0.
    OptionSet("label-type", [0], can_scale=False),
    # Fraction of features which are categorical
    OptionSet("frac-categorical-features", [0.5], can_scale=False),
    # Fraction of categorical features which are binary. Others have 20 categories.
    OptionSet("frac-binary-features", [0.5], can_scale=False),
    # Depth of true decision tree model used to label examples.
    # WARNING: The meaning of depth changed from Spark 1.0 to Spark 1.1:
    #          depth=N for Spark 1.0 should be depth=N-1 for Spark 1.1
    OptionSet("tree-depth", [5, 10, 15, 18], can_scale=False),
    # Maximum number of bins for the decision tree learning algorithm.
    OptionSet("max-bins", [32], can_scale=False),
    # Set algorithm to use: byRow = original MLlib, byCol = Yggdrasil
    OptionSet("alg-type", ["byRow", "byCol"]),
    # Ensemble types: DecisionTree
    #   Not yet supported: RandomForest, GradientBoostedTrees
    OptionSet("ensemble-type", ["DecisionTree"]),
    # Path to training dataset (if not given, use random data).
    #OptionSet("training-data", ["hdfs://ec2-54-86-227-115.compute-1.amazonaws.com:9000/data/mnist8m.scale"]),
    OptionSet("training-data", [""]),
    # Path to test dataset (only used if training dataset given).
    # If not given, hold out part of training data for validation.
    OptionSet("test-data", [""]),
    # Fraction of data to hold out for testing
    #  (Ignored if given training and test dataset, or if using synthetic data.)
    OptionSet("test-data-fraction", [0.2], can_scale=False),
    # Number of trees. If 1, then run DecisionTree. If >1, then run RandomForest.
    OptionSet("num-trees", [1], can_scale=False),
    # Feature subset sampling strategy: auto, all, sqrt, log2, onethird
    # (only used for RandomForest)
    OptionSet("feature-subset-strategy", ["auto"])
]

MLLIB_TESTS += [("decision-tree", MLLIB_PERF_TEST_RUNNER, SCALE_FACTOR,
    MLLIB_JAVA_OPTS, [ConstantOption("decision-tree")] +
    MLLIB_DECISION_TREE_TEST_OPTS)]