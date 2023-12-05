import os
from transformers import AutoTokenizer, AutoModelForCausalLM

# Set your Hugging Face API token
#os.environ['HF_API_TOKEN'] = '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'

# Load the Llama model
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

class PDFChatbot:
    def __init__(self, processed_text_file):
        with open(processed_text_file, 'r', encoding='utf-8') as file:
            self.processed_text = file.read()
        self.chat_history = []

    def get_response(self, user_query):
        # Update chat history for context
        self.chat_history.append(user_query)

        # Combine chat history with processed text for context
        combined_input = self.processed_text + " " + " ".join(self.chat_history[-3:])
        input_ids = tokenizer.encode(combined_input, return_tensors='pt', truncation=True, max_length=1024)

        # Generate response using Llama model
        output_ids = model.generate(input_ids, max_length=1024, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Update chat history with response
        self.chat_history.append(response)
        return response

# Example usage
chatbot = PDFChatbot('preprocessed_text.txt')
user_query = "Your question related to the PDF content"
response = chatbot.get_response(user_query)
print(response)
