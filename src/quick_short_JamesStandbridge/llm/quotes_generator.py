import json

from openai_chat import OpenAIChat

class QuotesGenerator:
    def __init__(self):
        self.model = OpenAIChat()

    def generate_quotes(self, keywords, trends, number_of_quotes):
        prompt = ("You have the pen of a great modern writer and fully understand what the audience on platforms "
          "like TikTok expects in terms of addictive content. I want you to generate a series of "+ str(number_of_quotes) +" quotes for "
          "a TikTok short that align with the following current trends: " + str(trends) + " and adhere to "
          "the following keywords: " + str(keywords) + ". I want each quote to be unique and generate 5 quotes, "
          "each no longer than a sentence, and send them to me in JSON format following this example format : [{\"us_quote\": \"quote translated in english\", \"arab_quote\": \"quote translated in arab\", \"fr_quote\": \"quote translated in french\"}]. Give me only the json output, nothing else, no message.")

        messages = [ 
            {'role': 'user', 'content': prompt}
        ]   

        response = self.model.query(messages, temperature=0.5, model="gpt-4")

        return json.loads(response.content)


def main():
    keywords = ['personal development', 'motivation', 'achievement']
    current_trends = ['#TheVoiceKids', '#Joblife', 'vingegaard', 'Pogacar', 'Barbie', 'Slimane', 'Alexandre Adler', 'Armstrong', 'DNCG', 'Textor', '#KCWIN', '#TDFF2023', 'Cyprien', 'Pogi', 'Van Aert']



    generator = QuotesGenerator()
    quotes = generator.generate_quotes(keywords, current_trends, 5)
    print(quotes)

if __name__ == "__main__":  
    main()