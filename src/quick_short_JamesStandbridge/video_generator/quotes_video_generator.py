from llm.quotes_generator import QuotesGenerator

class QuotesVideoGenerator:
    def __init__(self):
        pass

    def generate_from_keywords(self, keywords, trends, file_path, duration):
        quotes = QuotesGenerator().generate_quotes(keywords, trends, 5)

        print(quotes)

        pass


def main():
    keywords = ['personal development', 'motivation', 'achievement']
    current_trends = ['#TheVoiceKids', '#Joblife', 'vingegaard', 'Pogacar', 'Barbie', 'Slimane', 'Alexandre Adler', 'Armstrong', 'DNCG', 'Textor', '#KCWIN', '#TDFF2023', 'Cyprien', 'Pogi', 'Van Aert']

    generator = QuotesVideoGenerator()
    generator.generate_from_keywords(keywords, current_trends, "output.mp4", 60)

if __name__ == "__main__":
    main()