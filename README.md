# LangChain Course Directory Overview

This Markdown file provides a concise overview of each directory in the LangChain course, detailing the key focus and content of each.

## Directories

- `01_OpenAI_API`

  - Basic usage of the OpenAI API for generative AI applications.

- `02_LangChain_Inputs_and_Outputs`

  - Understanding the input and output mechanisms within LangChain.

- `03_Prompt_Templates`

  - Templates and best practices for effective prompting for OpenAI models.

- `04_Chains`

  - Detailed exploration of the Chains in LangChain with different use cases.

- `05_Callbacks`

  - Utilizing callback functions in LangChain for dynamic responses and interactions.

- `06_Memory`

  - Techniques and methods for implementing memory in generative AI models.

- `07_OpenAI_Functions`

  - OpenAI Function Calling with the OpenAI API and LangChain.

- `08_RAG`

  - Deep dive into Retrieval Augmented Generation (RAG) and its implementation in LangChain.

- `09_Agents`

  - Building and managing Autonomous Agents within the LangChain framework.

- `10_Hybrid_Search_and_Indexing_API`

  - Integration and use of Hybrid Search and the Indexing API for efficient data indexing.

- `11_LangSmith`

  - Leveraging LangSmith for Tracing, Datasets, and Evaluation.

- `12_MicroServiceArchitecture`

  - Understanding and applying microservice architecture in large language model (LLM) applications.

- `13_LangChain_ExpressionLanguage`
  - Exploring the LangChain Expression Language with the Runnable Interface.

Each directory is structured to provide learners with theoretical knowledge and practical insights, enabling a comprehensive understanding of LangChain and its applications in the field of generative AI.

---

### Additional Instructions

Clone the repository: [LangChain Udemy Course](https://github.com/Coding-Crashkurse/LangChain-Udemy-Course)

Please rename the `.env.example` to `.env` and provide your OpenAI API Key.

### Cleanup of Notebook output:

Linux: `find . -name "*.ipynb" -exec jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace {} \;`

Windows: `for /r %i in (*.ipynb) do jupyter nbconvert --to notebook --ClearOutputPreprocessor.enabled=True --inplace "%i"`
