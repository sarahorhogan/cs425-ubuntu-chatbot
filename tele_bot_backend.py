from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import pinecone
from transformers import AutoModel
from numpy.linalg import norm


app = Flask(__name__)

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("Arcpolar/Ubuntu_Llama_Chat_7B")
model = AutoModelForCausalLM.from_pretrained("Arcpolar/Ubuntu_Llama_Chat_7B", low_cpu_mem_usage=True)
# Set up the information retrieval system 
pinecone.init(api_key="c72b02c0-62fa-4ee2-aa36-6c2384fed7e1", environment="gcp-starter")
pinecone.list_indexes()
index = pinecone.Index("ubuntu-ir-jina")
cos_sim = lambda a,b: (a @ b.T) / (norm(a)*norm(b))
embedding_model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True) # trust_remote_code is needed to use the encode method

@app.route('/generate_response', methods=['POST'])
def generate_response():
    if request.method == 'POST':
        try:
            data = request.get_json()
            question = data.get('question')
            embedding = embedding_model.encode([question]).tolist()
            result = index.query(
            vector = embedding,
            top_k=1,
            include_metadata=True
            )
            context = str(result['matches'][0]['metadata']['text'])
            input = f'Context: {context} Question: {question}'
            if question:
                input_ids = tokenizer(input, return_tensors="pt").input_ids
                outputs = model.generate(input_ids, max_new_tokens=200)
                response = tokenizer.decode(outputs[0])

                return jsonify({'response': response})
            else:
                return jsonify({'error': 'Question not provided.'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
