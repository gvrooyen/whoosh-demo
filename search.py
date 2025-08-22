#!/usr/bin/env python3

import os
import sys
from typing import List, Dict, Tuple, Any
from bs4 import BeautifulSoup, Tag
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

def parse_faq_html(html_file: str) -> List[Dict[str, Any]]:
    """Parse the HTML file and extract FAQ entries."""

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    faq_items = soup.find_all('div', class_='faq-item')
    
    entries = []
    for item in faq_items:
        if not isinstance(item, Tag):
            continue
        category_elem = item.find('div', class_='category')
        question_elem = item.find('div', class_='faq-question')
        answer_elem = item.find('div', class_='faq-answer')
        
        if category_elem and question_elem and answer_elem:
            category = category_elem.get_text().strip()
            question = question_elem.get_text().strip()
            answer = answer_elem.get_text().strip()
            
            entries.append({
                'id': len(entries),
                'category': category,
                'question': question,
                'answer': answer,
                'content': f"{category} {question} {answer}"
            })
    
    return entries

def create_search_index(entries: List[Dict[str, Any]], index_dir: str) -> Any:
    """Create a Whoosh search index from FAQ entries."""

    schema = Schema(
        id=ID(stored=True),
        category=TEXT(stored=True),
        question=TEXT(stored=True),
        answer=TEXT(stored=True),
        content=TEXT
    )
    
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
    
    ix = index.create_in(index_dir, schema)
    
    writer = ix.writer()
    for entry in entries:
        writer.add_document(
            id=str(entry['id']),
            category=entry['category'],
            question=entry['question'],
            answer=entry['answer'],
            content=entry['content']
        )
    writer.commit()
    
    return ix

def search_faq(index_dir: str, query_string: str, limit: int = 3) -> List[Tuple[str, str, str]]:
    """Search the FAQ index and return results."""

    ix = index.open_dir(index_dir)
    
    with ix.searcher() as searcher:
        parser = QueryParser("content", ix.schema)
        query = parser.parse(query_string)
        results = searcher.search(query, limit=limit)
        
        return [(hit['question'], hit['answer'], hit['category']) for hit in results]

def main() -> None:
    html_file = 'faq.html'
    index_dir = 'indexdir'
    
    # Check if HTML file exists
    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found")
        sys.exit(1)
    
    print("Indexing FAQ entries...")
    
    # Parse FAQ entries
    entries = parse_faq_html(html_file)
    print(f"Found {len(entries)} FAQ entries")
    
    # Create search index
    create_search_index(entries, index_dir)
    print("Index created successfully!")
    
    # Interactive search
    while True:
        try:
            query = input("\nEnter search query (or 'quit' to exit): ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not query:
                continue
            
            results = search_faq(index_dir, query)
            
            if results:
                print(f"\nTop {len(results)} results:")
                print("-" * 50)
                for i, (question, answer, category) in enumerate(results, 1):
                    print(f"{i}. [{category}] {question}")
                    print(f"   {answer}")
                    print()
            else:
                print("No results found. Try a different search term.")
                
        except EOFError:
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
