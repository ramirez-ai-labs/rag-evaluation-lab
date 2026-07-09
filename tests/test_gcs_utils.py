"""Unit tests for lib/gcs_utils.py.

All GCS calls are mocked -- these tests never touch real credentials or
buckets, so they run for free and don't require `gcloud auth` locally.
"""

import io
import json
import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from lib import gcs_utils


class GcsUtilsTestCase(unittest.TestCase):
    def setUp(self):
        # The module caches a storage.Client() singleton across calls; reset
        # it before each test so one test's mock client can't leak into the next.
        gcs_utils._client = None

    @patch("lib.gcs_utils.storage.Client")
    def test_upload_corpus_writes_json_and_returns_uri(self, mock_client_cls):
        mock_blob = MagicMock()
        mock_client_cls.return_value.bucket.return_value.blob.return_value = mock_blob

        docs = ["doc one", "doc two"]
        uri = gcs_utils.upload_corpus(docs, "my-bucket")

        mock_blob.upload_from_string.assert_called_once_with(
            json.dumps(docs), content_type="application/json"
        )
        self.assertEqual(uri, "gs://my-bucket/corpus/documents.json")

    @patch("lib.gcs_utils.storage.Client")
    def test_load_or_compute_embeddings_cache_hit_skips_compute_fn(self, mock_client_cls):
        cached = np.array([[1.0, 2.0], [3.0, 4.0]])
        buf = io.BytesIO()
        np.save(buf, cached)

        mock_blob = MagicMock()
        mock_blob.exists.return_value = True
        mock_blob.download_as_bytes.return_value = buf.getvalue()
        mock_client_cls.return_value.bucket.return_value.blob.return_value = mock_blob

        compute_fn = MagicMock(side_effect=AssertionError("compute_fn should not run on a cache hit"))
        embeddings, latency_ms = gcs_utils.load_or_compute_embeddings("my-bucket", "path.npy", compute_fn)

        np.testing.assert_array_equal(embeddings, cached)
        self.assertEqual(latency_ms, 0.0)
        compute_fn.assert_not_called()

    @patch("lib.gcs_utils.storage.Client")
    def test_load_or_compute_embeddings_cache_miss_computes_and_uploads(self, mock_client_cls):
        computed = np.array([[5.0, 6.0]])
        mock_blob = MagicMock()
        mock_blob.exists.return_value = False
        mock_client_cls.return_value.bucket.return_value.blob.return_value = mock_blob

        compute_fn = MagicMock(return_value=(computed, 123.4))
        embeddings, latency_ms = gcs_utils.load_or_compute_embeddings("my-bucket", "path.npy", compute_fn)

        compute_fn.assert_called_once()
        np.testing.assert_array_equal(embeddings, computed)
        self.assertEqual(latency_ms, 123.4)
        mock_blob.upload_from_file.assert_called_once()


if __name__ == "__main__":
    unittest.main()
