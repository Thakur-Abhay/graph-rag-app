import streamlit as st
import openai
import os
from dotenv import load_dotenv
from graph_db import create_sample_graph, retrieve_relevant_nodes

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize graph
graph = create_sample_graph()

def graph_rag_response(query):
    relevant_nodes = retrieve_relevant_nodes(graph, query)
    context = "\n".join([f"- {text}" for _, text in relevant_nodes])

    prompt = f"""
    Answer the following query based on the provided context:
    
    Context:
    {context}

    Query:
    {query}

    Response:
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message['content']

# Streamlit App
st.title("🧠 Graph RAG Demo App")

user_query = st.text_input("Enter your query:", "")

if st.button("Generate Answer") and user_query.strip():
    with st.spinner("Fetching from Graph Database and Generating Answer..."):
        answer = graph_rag_response(user_query)
        st.markdown("### Generated Answer:")
        st.write(answer)

        st.markdown("### Context Retrieved from Graph Database:")
        context_nodes = retrieve_relevant_nodes(graph, user_query)
        for node, text in context_nodes:
            st.markdown(f"- **Node {node}:** {text}")
