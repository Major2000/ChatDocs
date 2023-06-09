import os
from langchain import OpenAI
from llama_index import (
    GPTSimpleVectorIndex,
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext,
    QuestionAnswerPrompt,
)

os.environ["OPENAI_API_KEY"] = "YOUR-API-KEY"

documents = SimpleDirectoryReader("documents").load_data()

llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))

service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)

index.save_to_disk('index.json')

index = GPTSimpleVectorIndex.load_from_disk('index.json', llm_predictor=llm_predictor)

QA_PROMPT_TMPL = (

        "Context information is below. \n"
        "---------------------\n"
                "{context_str}"
        "\n---------------------\n" 
        "Given this information, please answer the question: {query_str}\n"
        )

QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)

query_str = "What is the mission of the company?"
response = index.query(query_str, text_qa_template=QA_PROMPT)
print(response)
