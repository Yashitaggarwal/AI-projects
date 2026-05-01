import streamlit as st
import torch
from transformers import pipeline, BertTokenizer, BertForNextSentencePrediction
from sentence_transformers import SentenceTransformer, util

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="BERT Omniverse | Masterclass",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS FOR STYLING
# ==========================================
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem !important;
        font-weight: 800;
        background: -webkit-linear-gradient(#1E88E5, #004D40);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .task-header {
        font-size: 2.5rem !important;
        font-weight: 700;
        color: #004D40;
        border-bottom: 3px solid #1E88E5;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #1E88E5;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #004D40;
        border-color: #004D40;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# MODEL LOADING (CACHED)
# ==========================================
@st.cache_resource(show_spinner="Loading Sentiment Model...")
def load_sentiment():
    return pipeline("sentiment-analysis")

@st.cache_resource(show_spinner="Loading NER Model...")
def load_ner():
    return pipeline("ner", aggregation_strategy="simple")

@st.cache_resource(show_spinner="Loading QA Model...")
def load_qa():
    return pipeline("question-answering")

@st.cache_resource(show_spinner="Loading MLM Model...")
def load_mlm():
    return pipeline("fill-mask", model="bert-base-uncased")

@st.cache_resource(show_spinner="Loading Sentence Transformer...")
def load_sentence_transformer():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource(show_spinner="Loading NSP Model...")
def load_nsp():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForNextSentencePrediction.from_pretrained('bert-base-uncased')
    return tokenizer, model

@st.cache_resource(show_spinner="Loading Summarization Model...")
def load_summarization():
    return pipeline("summarization")

@st.cache_resource(show_spinner="Loading Zero-Shot Model...")
def load_zero_shot():
    return pipeline("zero-shot-classification")

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.image("https://huggingface.co/front/assets/huggingface_logo-noborder.svg", width=150)
st.sidebar.title("Navigation")
task = st.sidebar.radio(
    "Explore BERT Capabilities:",
    [
        "🏠 Home",
        "1️⃣ Text Classification (Sentiment)",
        "2️⃣ Named Entity Recognition (NER)",
        "3️⃣ Question Answering (QA)",
        "4️⃣ Masked Language Modeling (MLM)",
        "5️⃣ Next Sentence Prediction (NSP)",
        "6️⃣ Semantic Similarity",
        "7️⃣ Text Summarization",
        "8️⃣ Zero-Shot Classification"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Built with Streamlit & HuggingFace Transformers. Designed to showcase the complete power of BERT architectures.")

# ==========================================
# MAIN CONTENT
# ==========================================

if task == "🏠 Home":
    st.markdown('<div class="main-header">🤖 The BERT Omniverse</div>', unsafe_allow_html=True)
    st.markdown("""
    Welcome to the **BERT Masterclass Application**! 
    
    This application demonstrates the incredible versatility of **Bidirectional Encoder Representations from Transformers (BERT)** and its evolved variants.
    
    ### 🧠 What is BERT?
    BERT revolutionized Natural Language Processing (NLP) by introducing a truly bidirectional approach to language understanding. Instead of reading text linearly (left-to-right or right-to-left), BERT processes the entire context of a word simultaneously using the Transformer encoder architecture.
    
    ### 🚀 Explore the Capabilities:
    Use the sidebar to navigate through various NLP tasks, ranging from basic pre-training objectives to advanced downstream applications:
    
    1. **Text Classification:** Determine the sentiment of a text.
    2. **Named Entity Recognition (NER):** Extract entities like Persons, Organizations, and Locations.
    3. **Question Answering:** Extract exact answers from a given context.
    4. **Masked Language Modeling (MLM):** Predict missing words in a sentence (BERT's core pre-training task).
    5. **Next Sentence Prediction (NSP):** Determine if two sentences logically follow each other.
    6. **Semantic Similarity:** Measure how similar two pieces of text are using Sentence-BERT.
    7. **Text Summarization:** Condense long articles into short summaries.
    8. **Zero-Shot Classification:** Classify text into arbitrary categories without specific training.
    """)
    st.image("https://jalammar.github.io/images/bert-tasks.png", caption="Common BERT Downstream Tasks (Source: Jay Alammar)")

elif task == "1️⃣ Text Classification (Sentiment)":
    st.markdown('<div class="task-header">Text Classification (Sentiment Analysis)</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>How it works:</strong> A special <code>[CLS]</code> token is added at the beginning of the text. The final hidden state of this token is used as the aggregate sequence representation for classification tasks.</div>', unsafe_allow_html=True)
    
    classifier = load_sentiment()
    
    user_input = st.text_area("Enter text to analyze:", "I absolutely love working with Transformer models. They are incredibly powerful!")
    if st.button("Analyze Sentiment"):
        if user_input:
            with st.spinner("Analyzing..."):
                result = classifier(user_input)[0]
                label = result['label']
                score = result['score']
                
                if label == "POSITIVE":
                    st.success(f"Sentiment: **{label}** (Confidence: {score:.4f})")
                else:
                    st.error(f"Sentiment: **{label}** (Confidence: {score:.4f})")

elif task == "2️⃣ Named Entity Recognition (NER)":
    st.markdown('<div class="task-header">Named Entity Recognition (Token Classification)</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>How it works:</strong> The final hidden state of <strong>each token</strong> is fed into a classification layer over the NER label set. This allows the model to identify Persons, Organizations, Locations, etc.</div>', unsafe_allow_html=True)
    
    ner = load_ner()
    
    user_input = st.text_area("Enter text to extract entities:", "Hugging Face Inc. is a company based in New York City. Its founders include Clément Delangue and Julien Chaumond.")
    if st.button("Extract Entities"):
        if user_input:
            with st.spinner("Extracting..."):
                results = ner(user_input)
                if results:
                    st.write("### Identified Entities:")
                    for res in results:
                        st.info(f"**{res['word']}**  ➔  *{res['entity_group']}* (Confidence: {res['score']:.4f})")
                else:
                    st.warning("No entities found.")

elif task == "3️⃣ Question Answering (QA)":
    st.markdown('<div class="task-header">Extractive Question Answering</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>How it works:</strong> The model takes a Question and a Context as input <code>[CLS] Question [SEP] Context [SEP]</code>. It predicts two probabilities for each token: the likelihood of being the <strong>start</strong> of the answer span, and the <strong>end</strong> of the answer span.</div>', unsafe_allow_html=True)
    
    qa = load_qa()
    
    context = st.text_area("Context:", "Transformers is a state-of-the-art machine learning library for PyTorch, TensorFlow, and JAX. It provides APIs to easily download and train state-of-the-art pretrained models. Using pretrained models can reduce your compute costs, carbon footprint, and save you time from training a model from scratch.", height=150)
    question = st.text_input("Question:", "What does the Transformers library help reduce?")
    
    if st.button("Get Answer"):
        if context and question:
            with st.spinner("Searching for answer..."):
                result = qa(question=question, context=context)
                st.success(f"**Answer:** {result['answer']}")
                st.write(f"*Confidence Score:* {result['score']:.4f}")

elif task == "4️⃣ Masked Language Modeling (MLM)":
    st.markdown('<div class="task-header">Masked Language Modeling (MLM)</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>How it works:</strong> This is BERT\\'s primary pre-training objective. During pre-training, 15% of the tokens are masked. The model learns to predict these masked words based on the bidirectional surrounding context.</div>', unsafe_allow_html=True)
    
    mlm = load_mlm()
    
    st.info("Use `[MASK]` in your sentence to indicate the missing word.")
    user_input = st.text_input("Enter a sentence with [MASK]:", "The capital of France is [MASK] and it is a beautiful city.")
    
    if st.button("Fill the Mask"):
        if user_input and "[MASK]" in user_input:
            with st.spinner("Predicting..."):
                results = mlm(user_input)
                st.write("### Top Predictions:")
                for res in results:
                    st.success(f"**{res['token_str']}** (Score: {res['score']:.4f}) ➔ *{res['sequence']}*")
        else:
            st.error("Please ensure your sentence contains the exactly formatted `[MASK]` token.")

elif task == "5️⃣ Next Sentence Prediction (NSP)":
    st.markdown('<div class="task-header">Next Sentence Prediction (NSP)</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>How it works:</strong> BERT receives pairs of sentences. It uses the <code>[CLS]</code> token to predict if the second sentence logically follows the first sentence in the original document. This helps BERT understand relationships between sentences.</div>', unsafe_allow_html=True)
    
    tokenizer, model = load_nsp()
    
    col1, col2 = st.columns(2)
    with col1:
        sent1 = st.text_area("Sentence A:", "The sky is clear and the sun is shining brightly.")
    with col2:
        sent2 = st.text_area("Sentence B:", "It is a perfect day for a picnic in the park.")
        
    if st.button("Check Relationship"):
        if sent1 and sent2:
            with st.spinner("Evaluating relationship..."):
                encoding = tokenizer(sent1, sent2, return_tensors='pt')
                outputs = model(**encoding)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=1)
                
                # 0: IsNextSentence, 1: IsNotNextSentence
                is_next = probs[0][0].item()
                is_not_next = probs[0][1].item()
                
                if is_next > is_not_next:
                    st.success(f"**Logical Continuation!** Sentence B follows Sentence A. (Confidence: {is_next:.4f})")
                else:
                    st.error(f"**Unrelated.** Sentence B does NOT follow Sentence A. (Confidence: {is_not_next:.4f})")

elif task == "6️⃣ Semantic Similarity":
    st.markdown('<div class="task-header">Semantic Similarity (Sentence-BERT)</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>How it works:</strong> Standard BERT is computationally expensive for comparing many sentences (requires NxN forward passes). <strong>Sentence-BERT (SBERT)</strong> modifies the BERT network using Siamese and triplet network structures to derive semantically meaningful sentence embeddings that can be compared using cosine similarity.</div>', unsafe_allow_html=True)
    
    sbert = load_sentence_transformer()
    
    col1, col2 = st.columns(2)
    with col1:
        text1 = st.text_area("Text 1:", "A man is playing a guitar.")
    with col2:
        text2 = st.text_area("Text 2:", "A man is strumming an acoustic guitar.")
        
    if st.button("Calculate Similarity"):
        if text1 and text2:
            with st.spinner("Calculating embeddings..."):
                emb1 = sbert.encode(text1, convert_to_tensor=True)
                emb2 = sbert.encode(text2, convert_to_tensor=True)
                
                cosine_scores = util.cos_sim(emb1, emb2)
                score = cosine_scores[0][0].item()
                
                st.progress(score)
                st.write(f"### Cosine Similarity Score: **{score:.4f}**")
                
                if score > 0.8:
                    st.success("These sentences are highly similar!")
                elif score > 0.5:
                    st.warning("These sentences are somewhat similar.")
                else:
                    st.error("These sentences are quite different.")

elif task == "7️⃣ Text Summarization":
    st.markdown('<div class="task-header">Text Summarization (Seq2Seq)</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>How it works:</strong> While base BERT is an encoder-only model, sequence-to-sequence variants like BART (Bidirectional and Auto-Regressive Transformers) combine a bidirectional encoder (like BERT) with an autoregressive decoder (like GPT) to generate abstractive summaries.</div>', unsafe_allow_html=True)
    
    summarizer = load_summarization()
    
    article = st.text_area("Enter a long article to summarize:", "The James Webb Space Telescope is a space telescope designed primarily to conduct infrared astronomy. As the largest telescope in space, it is equipped with high-resolution and highly sensitive instruments, allowing it to view objects too old, distant, or faint for the Hubble Space Telescope. This will enable investigations across many fields of astronomy and cosmology, such as observation of the first stars and the formation of the first galaxies, and detailed atmospheric characterization of potentially habitable exoplanets.", height=200)
    
    if st.button("Summarize"):
        if article:
            with st.spinner("Summarizing..."):
                summary = summarizer(article, max_length=50, min_length=10, do_sample=False)
                st.write("### Summary:")
                st.info(summary[0]['summary_text'])

elif task == "8️⃣ Zero-Shot Classification":
    st.markdown('<div class="task-header">Zero-Shot Classification</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><strong>How it works:</strong> Using Natural Language Inference (NLI), we can classify a text into categories the model has never explicitly been trained on. It treats the input text as the premise and the candidate categories as hypotheses.</div>', unsafe_allow_html=True)
    
    zsc = load_zero_shot()
    
    sequence = st.text_area("Text to classify:", "I just bought a new graphics card and the 3D rendering speed is absolutely incredible!")
    labels_input = st.text_input("Candidate labels (comma-separated):", "technology, sports, politics, food")
    
    if st.button("Classify"):
        if sequence and labels_input:
            labels = [label.strip() for label in labels_input.split(',') if label.strip()]
            with st.spinner("Classifying..."):
                result = zsc(sequence, candidate_labels=labels)
                st.write("### Classification Results:")
                for label, score in zip(result['labels'], result['scores']):
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.write(f"**{label}**")
                    with col2:
                        st.progress(float(score))
                        st.write(f"{score*100:.2f}%")
