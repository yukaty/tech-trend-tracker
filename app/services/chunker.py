import nltk
from typing import List

class ArticleChunker:
    """ Create chunks of text from an article """

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def create_chunks(self, article_text: str) -> List[str]:
        # Tokenize the article text into sentences
        sentences = nltk.sent_tokenize(article_text)
        chunks = []
        current_chunk = []
        current_size = 0

        for sentence in sentences:
            sentence_len = len(sentence)

            if current_size + sentence_len > self.chunk_size:
                # Add the current chunk to the list if it's too big
                chunk_text = ' '.join(current_chunk)
                chunks.append(chunk_text)

                # Reset the current chunk
                overlap_tokens = current_chunk[-2:] if len(current_chunk) > 2 else current_chunk
                current_chunk = overlap_tokens + [sentence]
                current_size = sum(len(s) for s in current_chunk)
            else:
                # Add the sentence to the current chunk
                current_chunk.append(sentence)
                current_size += sentence_len

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks