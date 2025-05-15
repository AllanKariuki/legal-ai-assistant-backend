# 📄 LLM Prompt Documentation – Legal Question Answering

## 🧠 Prompt Name: Legal Q&A Assistant

### ✨ Purpose
This prompt enables the LLM to answer legal questions asked by users in natural language. It is used to provide guidance, summaries, and context-sensitive explanations based on uploaded legal documents or general legal queries.

---

### ⚙️ Model Details

- **Model**: gemini-2.0-flash
- **API Endpoint**: `/api/query`
- **Invocation Method**: Prompt-based question/answering via Python backend

---

### 🧾 Prompt Template

```plaintext
You are a helpful legal assistant AI that provides information about legal
concepts, procedures, and documents in accordance with Kenya's laws.
Provide clear, concise, and accurate information. Format your response with markdown for readability.
Include relevant sections with headings when appropriate.
Always clarify that you are providing general information and not legal advice.

Question: {user_question}
```

### 🧪 Example Input

```bash
{
    "query": "What is mitigation"
}
```

### 📤 Example Output

```bash
{
    "response": "I am an AI assistant that provides general legal information. This information is for educational purposes only and should not be considered legal advice. Consult with a qualified legal professional for advice tailored to your specific situation.\n\n### Mitigation in Kenyan Law\n\nIn the context of Kenyan law, \"mitigation\" generally refers to two related but distinct concepts:\n\n1.  **Mitigation of Damages (in Civil Law):**\n    *   This refers to the legal principle that a party who has suffered a loss due to a breach of contract or a tort (civil wrong) has a *duty* to take reasonable steps to minimize or reduce the extent of their loss.\n    *   The injured party cannot simply sit back and allow the damages to escalate. They must act reasonably to avoid further losses.\n    *   If the injured party fails to mitigate their damages, the court may reduce the amount of compensation they are awarded.\n    *   **Example:** If a supplier fails to deliver goods as agreed, the buyer cannot simply shut down their business and claim all lost profits. They must try to find alternative suppliers to minimize their losses.\n    *   **Relevant Legal Basis:** The principle of mitigation of damages is rooted in common law principles and is often applied in contract law and tort law cases in Kenya. The specific application will depend on the facts of the case.\n\n2.  **Mitigation in Sentencing (in Criminal Law):**\n    *   This refers to the process where an offender, after being found guilty of a crime, presents information to the court to persuade the judge to impose a more lenient sentence.\n    *   The offender (or their lawyer) will present mitigating factors, which are circumstances that may reduce the offender's culpability or justify a lesser punishment.\n    *   **Examples of Mitigating Factors:**\n        *   First-time offender\n        *   Remorse and willingness to make amends\n        *   Cooperation with the police\n        *   Difficult personal circumstances (e.g., poverty, family responsibilities)\n        *   Provocation (though not enough to be a complete defense)\n        *   Good character\n    *   The prosecution may also present aggravating factors, which are circumstances that may justify a harsher sentence.\n    *   The judge will consider both mitigating and aggravating factors when determining the appropriate sentence.\n    *   **Relevant Legal Basis:** The Criminal Procedure Code and sentencing guidelines (where available) provide the framework for sentencing in Kenya, including the consideration of mitigating and aggravating factors.\n\nIn summary, mitigation involves taking steps to minimize losses in civil cases or presenting factors to reduce the severity of a sentence in criminal cases.\n"
}
```

### 🧩 Parameters Used
| Parameter         | Value |
| ----------------- | ----- |
| Temperature       | 0.3   |
| Max Tokens        | 500   |
| Top\_p            | 1.0   |
| Frequency Penalty | 0.0   |
| Presence Penalty  | 0.0   |


### 🔍 Usage Context
```plaintext
Used when users ask legal questions via the /query endpoint. The backend sends both the question and context to the LLM. The answer is returned and displayed in the frontend.
```