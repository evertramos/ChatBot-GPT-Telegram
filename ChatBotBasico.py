import langchain 
from aiogram import Bot, Dispatcher, executor, types


loader = langchain.document_loaders.DirectoryLoader('TelegramBOT/ArquivosTXT/', 
                                                    glob="**/*.txt", 
                                                    loader_cls=langchain.document_loaders.TextLoader)
documents = loader.load()
len(documents)
text_splitter = langchain.text_splitter.RecursiveCharacterTextSplitter(chunk_size =2300, 
                                                                       chunk_overlap  =10, 
                                                                       length_function =len, 
                                                                       separators="\n\n")
texts = text_splitter.split_documents(documents)

Mensagem =['Mensagem']
Pergunta = ['Pergunta']

def query_gpt(input):
    embeddings = langchain.embeddings.OpenAIEmbeddings(openai_api_key = '')
    doc_search = langchain.vectorstores.Chroma.from_documents(texts, embeddings)
    chain = langchain.VectorDBQA.from_chain_type(llm=langchain.OpenAI(openai_api_key = ''), 
                                                 chain_type = 'stuff', 
                                                 vectorstore = doc_search)
    Mensagem[0] = chain.run(input)

bot = Bot(token = 'SEU_TOKEN')
dp = Dispatcher(bot)

@dp.message_handler()
async def gpt(message:types.message):
    query_gpt(message.text)
    await message.reply(Mensagem[0])

if __name__ =='__main__':
    executor.start_polling(dp) 
