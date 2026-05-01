# 🤖 BERT Omniverse: The Ultimate Masterclass Application

Welcome to the **BERT Omniverse**, a comprehensive Streamlit application designed to showcase the full spectrum of capabilities of the **Bidirectional Encoder Representations from Transformers (BERT)** architecture and its variants.

This project goes from the "bare minimum" foundational concepts of BERT to its "maximum" utility across various complex Natural Language Processing (NLP) tasks.

## 🌟 Features / Tasks Covered

### 1. Text Classification (Sentiment Analysis)
- **Concept:** Uses the `[CLS]` token's final hidden state to predict the category or sentiment of an entire sequence.
- **App Usage:** Input any text, and the model will classify it as POSITIVE or NEGATIVE along with a confidence score.

### 2. Named Entity Recognition (NER)
- **Concept:** Token Classification. The model analyzes the final hidden state of *each token* to classify whether it belongs to a specific entity (Person, Organization, Location, etc.).
- **App Usage:** Paste an article or sentence, and the app will extract and highlight the named entities.

### 3. Extractive Question Answering (QA)
- **Concept:** The model is fed a `[Question]` + `[SEP]` + `[Context]`. It outputs two probability distributions: one for the start of the answer span and one for the end of the answer span within the context.
- **App Usage:** Provide a paragraph of text and ask a specific question related to it.

### 4. Masked Language Modeling (MLM)
- **Concept:** This is how BERT is pre-trained. 15% of the input tokens are masked, and the bidirectional encoder predicts the masked word based on both left and right contexts.
- **App Usage:** Type a sentence containing `[MASK]` (e.g., "The capital of France is [MASK].") and see the model's top predictions.

### 5. Next Sentence Prediction (NSP)
- **Concept:** Another pre-training task for BERT. Given two sentences A and B, the model uses the `[CLS]` token to predict if B logically follows A in the original document.
- **App Usage:** Enter two sentences and evaluate their sequential relationship.

### 6. Semantic Similarity (Sentence-BERT)
- **Concept:** Standard BERT is extremely slow for comparing large numbers of sentences. Sentence-BERT adds a pooling layer to generate fixed-sized sentence embeddings, allowing for lightning-fast cosine similarity comparisons.
- **App Usage:** Enter two sentences and get a cosine similarity score (0 to 1) representing how semantically similar they are.

### 7. Text Summarization
- **Concept:** While pure BERT is an encoder-only model (not meant for generation), its descendant architectures like BART (Bidirectional and Auto-Regressive Transformers) pair a BERT-like encoder with an autoregressive decoder to perform abstractive summarization.
- **App Usage:** Paste a long document and get a concise summary.

### 8. Zero-Shot Classification
- **Concept:** Using Natural Language Inference (NLI), we can classify text into categories the model has never explicitly been trained on, by treating the input text as the premise and the categories as hypotheses.
- **App Usage:** Provide an input text and a comma-separated list of candidate labels to see the classification probabilities.

## 🚀 Installation & Setup

1. **Navigate to the Directory**
   ```bash
   cd c:\Users\yashi\OneDrive\Desktop\AGENTICAI\bert_omniverse
   ```
2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   # Activate on Windows:
   venv\Scripts\activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## 📦 Requirements

- `streamlit`: For the interactive web interface.
- `transformers`: Hugging Face library providing the BERT models and pipelines.
- `torch`: PyTorch backend required by Transformers.
- `sentence-transformers`: Specialized library for generating sentence embeddings via Sentence-BERT.

*Note: The first time you interact with specific tasks in the app, it will download the necessary pre-trained weights from Hugging Face. This may take some time depending on your internet connection.*
