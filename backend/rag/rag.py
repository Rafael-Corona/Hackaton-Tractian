from typing import List
from pypdf import PdfReader

import faiss
from langchain.schema.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.docstore.in_memory import InMemoryDocstore

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 



class RAG:
    vector_store = None
    llm = None
    memory = None
    conversation_chain = None
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        index = faiss.IndexFlatL2(len(self.embeddings.embed_query("hello world")))
        self.vector_store = FAISS(
            embedding_function=self.embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-4")
        self.memory = ConversationBufferMemory(
            memory_key='chat_history', return_messages=True
        )
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            memory=self.memory,
            max_tokens_limit=8000,
        )
        
    def add_documents(self, documents: List[str]):
        for doc in documents:
            reader = PdfReader(doc)

            full_txt = ''
            for page in reader.pages:
                full_txt += page.extract_text()
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200, add_start_index=True
            )

            # text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=20)
            docs = [Document(page_content=x) for x in text_splitter.split_text(full_txt)]

            data = text_splitter.split_documents(docs)
            self.vector_store.add_documents(documents=data)
    
    def query(self, q:str) -> str:
        # todo: traduzir do portugues <=> ingles
        result = self.conversation_chain({"question": q})
        answer = result["answer"]
        return answer
    
if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    rag = RAG()
    docs = []
    target_folder = 'data/documents/technical-catalog'
    for file in os.listdir(target_folder):
        docs.append(f'{target_folder}/{file}')
        
    rag.add_documents(docs)
    print(rag.query('What is the best option to maintain energy supply?'))
    



            