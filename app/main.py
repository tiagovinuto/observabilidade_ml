
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram, Counter, Gauge
import time
from modules.sentiment_features import Sentiment_features
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from googletrans import Translator
import nltk

# Download do recurso "brown" do NLTK
nltk.download('brown')

# Download de todos os recursos necessários para o TextBlob
from textblob.download_corpora import download_all
download_all()

# Inicialização da aplicação FastAPI
app = FastAPI()

# Configuração das métricas Prometheus
polarity_gauge = Gauge('polarity', 'Polaridade do sentimento da frase')
subjectivity_gauge = Gauge('subjectivity', 'Subjetividade do sentimento da frase')
word_count_counter = Counter('word_count', 'Contagem de palavras na frase')
sentence_count_counter = Counter('sentence_count', 'Contagem de sentenças na frase')
keyword_count_counter = Counter('keyword_count', 'Contagem de ocorrências da palavra-chave na frase')
named_entities_gauge = Gauge('named_entities', 'Número de entidades nomeadas na frase')
topics_gauge = Gauge('topics', 'Número de tópicos principais na frase')
model_prediction_latency = Histogram('modelo_prediction_latency_seconds', 'Model Prediction Latency (seconds)')

# Rota principal para a página inicial
@app.get('/')
def home():
    return "Observação de modelos de ML - Análise de Sentimentos"

# Rota para a análise de sentimento
@app.post('/analise_sentimento/')
async def predict_banck_features(data: Sentiment_features) -> str:
    start_time = time.time()

    frase = data.frase
    
    translator = Translator()
    frase_en = translator.translate(frase, dest='en')
    frase_en_text = frase_en.text
    tb = TextBlob(frase_en_text)

    finish_time = time.time()
    
    tb_with_analyzer = TextBlob(frase_en.text, analyzer=NaiveBayesAnalyzer())
    
    prediction_time = finish_time - start_time
    model_prediction_latency.observe(prediction_time)  # Observa o tempo de predição

    # Cálculo das métricas
    polarity = tb.sentiment.polarity
    subjectivity = tb.sentiment.subjectivity
    word_count = len(tb.words)
    sentence_count = len(tb.sentences)
    keyword_count = tb.words.count(frase)
    named_entities = len(tb.noun_phrases)
    topics = len(tb_with_analyzer.noun_phrases)

    # Exporta as métricas para o Prometheus
    polarity_gauge.set(polarity)
    subjectivity_gauge.set(subjectivity)
    word_count_counter.inc(word_count)
    sentence_count_counter.inc(sentence_count)
    keyword_count_counter.inc(keyword_count)
    named_entities_gauge.set(named_entities)
    topics_gauge.set(topics)

    if tb.sentiment.polarity > 0.5:
        return "Positivo"
    else:
        return "Negativo"

# Configuração do middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Instrumentator().instrument(app).expose(app) # Instrumenta e expõe a aplicação para o Prometheus