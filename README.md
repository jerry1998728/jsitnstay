# 🐶 J.Sit & Stay – Multi-Agent RAG-Powered Chatbot Assistant

J.Sit & Stay is an intelligent, multi-agent chatbot built to automate and streamline customer intake and service for a pet-sitting business. Powered by cutting-edge GenAI technologies, the assistant answers user questions, processes bookings, and provides personalized care insights — reducing manual input and elevating the client experience.

---

## Overview

This chatbot assistant was designed to:
- Automate customer inquiries about services, pricing, and pet care.
- Streamline intake forms and background collection with dynamic logic.
- Reduce repetitive manual tasks for business owners using LLM-driven interaction.
- Integrate domain-specific knowledge using a RAG (Retrieval-Augmented Generation) pipeline.

---

## Tech Stack

| Tool | Description |
|------|-------------|
| **OpenAI GPT-3.5 Turbo** | Language model for generating conversational responses |
| **ADA-002** | Embedding model for semantic search and similarity |
| **Pinecone** | Vector database for storing and retrieving contextually relevant business data |
| **Streamlit** | Lightweight, chat-style frontend interface |
| **Render** | Deployment platform for hosting the chatbot |
| **Prompt Engineering** | Tailored prompts per agent to ensure accurate, role-specific outputs |

---

## System Design

### Multi-Agent Architecture

The chatbot consists of **three specialized agents**:
1. **Booking Manager** – Handles client intake, schedule checks, and basic onboarding.
2. **Concierge Manager** – Answers business-specific FAQs using context from the RAG system.
3. **Public Relations Manager** – Responds to service quote questions and can escalate/flag negotiation cases.

### RAG Pipeline

- Embeds internal documents (e.g., Pricing, service policies, customer FAQs) using **ADA-002**
- Stores them in **Pinecone**
- Dynamically retrieves relevant chunks for each query
- Injects the context into GPT prompts to improve response accuracy

---

## Key Results

- **Reduced manual intake effort by ~90%**
- **Improved booking process efficiency by 100%**
- **Enhanced accuracy in policy-related responses through vector search**
- **Improved overall user engagement with intelligent, guided conversations**
- **Manual LLM Evaluation performed to ensure 100% accuracy with 0% hallucination, 100% expected Tone and Format, and 100% helpfulness in the final LLM Response**

---

## Author
Built by **Cheng-Tso (Jerry) Hsieh** in a timespan of a 10-day spring break 
🔗 [LinkedIn](https://linkedin.com/in/jerry-ct-hsieh) | 🐙 [GitHub](https://github.com/jerry1998728)

