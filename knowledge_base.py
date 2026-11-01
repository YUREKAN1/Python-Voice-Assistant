
import json
import re
from pathlib import Path
from difflib import get_close_matches


class KnowledgeBase:

    def __init__(self, file_path="knowledge.json"):
        self.file_path = Path(file_path)
        self.knowledge = []
        self.load_knowledge()

    def normalize(self, text):
        """Normalize text for comparison."""
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", "", text)
        return " ".join(text.split())

    def load_knowledge(self):
        """Load questions and answers from JSON."""

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.knowledge = data.get("knowledge", [])

        except FileNotFoundError:
            print("Knowledge file not found.")

        except json.JSONDecodeError:
            print("Invalid JSON format in knowledge.json.")

    def get_answer(self, question):
        """Find an answer using exact or fuzzy matching."""

        normalized_question = self.normalize(question)

        question_map = {}

        for item in self.knowledge:
            for phrase in item["questions"]:
                normalized_phrase = self.normalize(phrase)
                question_map[normalized_phrase] = item["answer"]

        # Exact match
        if normalized_question in question_map:
            return question_map[normalized_question]

        # Similarity matching
        matches = get_close_matches(
            normalized_question,
            question_map.keys(),
            n=1,
            cutoff=0.78
        )

        if matches:
            return question_map[matches[0]]

        return None


if __name__ == "__main__":

    kb = KnowledgeBase()

    question = input("Enter your question: ")

    answer = kb.get_answer(question)

    if answer:
        print("Answer:", answer)
    else:
        print("Sorry, I don't know the answer yet.")
