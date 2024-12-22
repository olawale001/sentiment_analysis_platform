import plotly.express as px
import pandas as pd
from vaderSentiment.vaderSentiment import  SentimentIntensityAnalyzer
from analysis.models import SentimentAnalysis

def analysis_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    if score['compound'] >= 0.05:
        sentiment = 'Positive'
    elif score['compound'] <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    return {"sentiment": sentiment, "confidence": abs(score['compound'])}

def analyze_csv(file_path):
    df = pd.read_csv(file_path)
    analyzer = SentimentIntensityAnalyzer()
    results = []

    for index, row in df.iterrows():
        text = row.get("text", "")
        if text:
            score = analyzer.polarity_scores(text)
            sentiment = (
                "Positive" if score["compound"] >= 0.05 else 
                "Negative" if score["_Compound"] <= -0.05 else
                "Neutral"
            )
            results.append({"text": text, "sentiment": sentiment, "confidence": abs(score["compound"])})

    return results   

def generate_sentiment_chart():
    data = SentimentAnalysis.objects.all().values("sentiment")
    df= pd.DataFrame(data)
    if df.empty:
        return None
    
    fig = px.pie(
        df, name="sentiment", title="Sentiment Distribution", 
        hole=0.3, color_discrete_sequence=px.colors.qualitative.Set3
    )
    return fig.to_html(full_html=False)