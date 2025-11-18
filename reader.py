import pdfplumber
import spacy
from typing import List, Dict
import re

class PDFReader:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_md")
        except OSError:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_md"])
            self.nlp = spacy.load("en_core_web_md")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        full_text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")
        return full_text
    
    def split_into_sentences(self, text: str) -> List[str]:
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        return sentences
    
    def find_intervention_sentences(self, sentences: List[str], keywords_dict: Dict) -> List[Dict]:
        found_interventions = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for intervention_type, keywords in keywords_dict.items():
                for keyword in keywords:
                    if keyword.lower() in sentence_lower:
                        found_interventions.append({
                            'intervention_type': intervention_type,
                            'sentence': sentence,
                            'matched_keyword': keyword
                        })
                        break
        return found_interventions
    
    def process_pdf(self, pdf_path: str, knowledge_base: Dict) -> List[Dict]:
        full_text = self.extract_text_from_pdf(pdf_path)
        sentences = self.split_into_sentences(full_text)
        keywords_dict = {}
        for intervention_type, config in knowledge_base.items():
            keywords_dict[intervention_type] = config['keywords']
        found_interventions = self.find_intervention_sentences(sentences, keywords_dict)
        return found_interventions
