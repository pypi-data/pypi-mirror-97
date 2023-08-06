// Copyright (c) FlapMX LLC.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

db.task.drop();
db.task.insertMany([
    {
        "label": "Named-Entity-Recognition",
        "value": "ner"
    }
]);

db.model.drop();
db.model.insertMany([
    {
        "task" : "ner",
        "models": [
            {
                "label": "PubMedBERT (BC5CDR-chem)",
                "value": "pubMedBERT_model_BC5CDR_chem"
            },
            {
                "label": "PubMedBERT (BC5CDR-disease)",
                "value": "pubMedBERT_model_BC5CDR_disease"
            },
            {
                "label": "PubMedBERT (BC2GM)",
                "value": "pubMedBERT_model_BC2GM"
            },
            {
                "label": "PubMedBERT (JNLPBA)",
                "value": "pubMedBERT_model_JNLPBA"
            },
            {
                "label": "PubMedBERT (NCBI)",
                "value": "pubMedBERT_model_NCBI"
            }]
    }
]);