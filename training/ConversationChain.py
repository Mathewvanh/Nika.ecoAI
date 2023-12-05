from transformers import AutoTokenizer, AutoModelForCausalLM
from answer import load_faiss_index, get_chunk_text
from embed import *
from process_query import *

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

class ConversationChain:
    def __init__(self):
        self.chat_history = []
        self.faiss_index = load_faiss_index()  # Load your FAISS index

    def process_query(self, query):
        # Process the query considering the chat history
        return process_query(query)

    def retrieve_relevant_chunks(self, query_embedding, k=5):
        _, indices = self.faiss_index.search(np.array([query_embedding]), k)
        return indices[0]

    def generate_answer(self, user_query, chunk_indices):
        # Retrieve relevant texts and combine them with user query
        relevant_texts = [get_chunk_text(index) for index in chunk_indices]
        combined_text = " ".join(relevant_texts)

        # Use Llama 2 model to generate the response
        input_text = user_query + " " + combined_text
        input_ids = tokenizer.encode(input_text, return_tensors='pt')
        output = model.generate(input_ids, max_length=512)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        return response

    def get_response(self, user_query):
        processed_query = self.process_query(user_query)
        query_embedding = get_embedding(processed_query)
        chunk_indices = self.retrieve_relevant_chunks(query_embedding)
        answer = self.generate_answer(user_query, chunk_indices)

        # Update chat history
        self.chat_history.append({"query": user_query, "answer": answer})
        return answer

# Example usage
conversation = ConversationChain()
user_query = "What are the verra methodologies"
response = conversation.get_response(user_query)
print(response)

# Follow-up query
follow_up_query = "which formulas do they use?"
follow_up_response = conversation.get_response(follow_up_query)
print(follow_up_response)
