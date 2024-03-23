import tensorflow as tf
from transformers import pipeline
import fetch
import emoji
import re

sentiment_pipeline = pipeline("sentiment-analysis")

def replace_emojis_with_names(text):
    def replace(match):
        emoji_unicode = match.group()
        try:
            emoji_name = emoji.demojize(emoji_unicode).replace(":", "")
        except KeyError:
            # If the emoji cannot be converted to a name, return the original
            return emoji_unicode
        return emoji_name

    # Regular expression to match emojis
    emoji_pattern = re.compile(r'[\U0001F300-\U0001F6FF\u2600-\u26FF\u2700-\u27BF]+', re.UNICODE)

    # Replace emojis with their names
    replaced_text = emoji_pattern.sub(replace, text)

    return replaced_text

def main():
    id = input('Provide a Amazon Product ID like this:\n\nB0CDC4X65Q\n\nID:')
    search_url = f"https://www.amazon.com/BERIBES-Cancelling-Transparent-Soft-Earpads-Charging-Black/product-reviews/{id}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    soup = fetch.get_soup(search_url)
    data = fetch.get_reviews(soup)

    messageData = []
    for review in data:
        messageData.append(replace_emojis_with_names(review['content']))

    analysis = sentiment_pipeline(messageData)

    for review, sentiment in zip(messageData, analysis):
        print(f"Review: \t{review}\nSentiment: {sentiment['label']}\nConfidence: {sentiment['score']*100}%\n\n")
    
    print("\n-----------------------------------------------------\n\n")
    averageScore = 0
    for sentiment in analysis:
        averageScore += sentiment['score'] * (1 if sentiment['label'] == 'POSITIVE' else 0)
    averageScore = averageScore / len(analysis)
    print(f"Average Score: {averageScore*100}%")
    print("Sentiment: Positive" if averageScore > .7 else "Sentiment: Negative" if averageScore < .4 else "Sentiment: Neutral")

if __name__ == "__main__":
    main()