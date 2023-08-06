from typing import Any, Optional, Union, List, Dict, Tuple
from .sampling_agent import SamplingAgent
from .dataset import LabeledDataset, LabeledFrame

import joblib
import json
import pandas as pd
import pyarrow as pa
import numpy as np
from sklearn.preprocessing import normalize


class EmbeddingDistanceSamplingAgent(SamplingAgent):
    def __init__(self, random_seed=None):
        self.random_seed = random_seed
        self.element_type = None

        self.pca = None
        self.microclusters = None
        self.microcluster_centroids = None
        self.microcluster_radii = None

    def load_sampling_dataset(
        self, element_type: str, preprocessed_info: Dict[str, Any]
    ) -> None:
        self.element_type = element_type  # "crop" or "frame"
        self.pca = joblib.load(preprocessed_info["pca_path"])

        df = pa.ipc.open_file(preprocessed_info["microcluster_info_path"]).read_pandas()
        self.microclusters = df["microclusters"].to_numpy().tolist()
        self.microcluster_centroids = df["microcluster_centroids"].to_numpy().tolist()
        self.microcluster_radii = df["microcluster_radii"].to_numpy().tolist()

    # Returns a dict with (similarity_score, similarity_score_version, sampled_element_id)
    def score_frame(self, frame: LabeledFrame) -> Dict[str, Any]:
        if not frame.embedding:
            raise Exception(
                "Frames for embedding distance sampling must have embeddings."
            )

        # List of {"uuid": ..., "embedding": ...} elements
        embeddings_to_score = []
        if self.element_type == "frame":
            if frame.embedding.get("embedding"):
                embeddings_to_score = [
                    {
                        "uuid": frame.embedding.get("task_id"),
                        "embedding": frame.embedding.get("embedding"),
                    }
                ]
            else:
                raise Exception(
                    f"Frames for embedding distance sampling must have valid, non-empty frame embedding."
                )
        else:  # crop
            if frame.embedding.get("crop_embeddings"):
                embeddings_to_score = [
                    e
                    for e in frame.embedding.get("crop_embeddings")
                    if e.get("embedding")
                ]

        max_score = 0
        max_score_elt = None

        for embedding_info in embeddings_to_score:
            element_id = embedding_info.get("uuid")
            raw_emb = embedding_info.get("embedding")

            wrapped = np.array([raw_emb])
            normalized = normalize(wrapped)
            vec = self.pca.transform(normalized)[0]

            for j in range(len(self.microclusters)):
                target_centroid = self.microcluster_centroids[j]
                dist = np.linalg.norm(vec - target_centroid)
                score = max(1 - dist / (2 * self.microcluster_radii[j]), 0)
                if score > max_score:
                    max_score = score
                    max_score_elt = element_id

        return {
            "similarity_score": max_score,
            "similarity_score_version": "v1",
            "sampled_element_id": max_score_elt,
        }
