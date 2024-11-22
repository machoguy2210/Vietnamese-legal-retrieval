# RAG-based Vietnamese Legal Retrieval

The pipelines for this project is shown as below:
Query --> Bi-encoder --> Cross-Encoder --> Top k documents --> LLM --> Answer

The data used for text retrieval was collected myself from the website [vbpl.vn](http://vbpl.vn), including 22,216 documents belonging to the following categories: Codes, Laws, Constitution, Decrees, Decisions, Ordinances, Circulars, and Joint Circular.
The documents were then preprocessed, chunked and stored in database.

I used the LLM to create the training data by feeding each chunk into the model and prompting it to generate new questions, resulting in (question, answer_chunks) pairs.

Test data was splitted from the generated data to evaluate the model.

Results are shown in the table below:

![image](https://github.com/user-attachments/assets/f27b06b1-6aec-410d-8867-2244500f1260)




