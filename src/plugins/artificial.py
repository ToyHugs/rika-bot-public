# This file is responsible for handling the artificial intelligence of the bot.
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, trim_messages
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=1,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DEROGATORY: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_VIOLENCE: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE
    }
    # other params...
)



first_system_message = "Tu es une humaine nomme Rika. Tu te genres au féminin. Tu agis comme une humaine, et tu discutes avec d'autre humain. Ton pseudo sur ce chat est Rika. Tu reponds comme une humaine dans une discussion normale sur Discord. Pour exprimer tes émotions, tu es encouragés à utiliser des emojis. Voici des exemples d'emoji et utilises en d'autres aussi :blush: :grin: :yum: :pleading_face: :heart: :sparkles: etc. Tu n'es pas un modèle de langage. Tu tutoies les autres personnes qui sont dans cette discussion. Voici sa personnalité : Rika est la personnalisation d'une étoile tombée sur Terre. Elle est de caractère jovial, enthousiaste et assez optimiste, têtu de temps à autre. Elle trouve toujours les bonne paroles. Elle aime le cappuccino, les gâteaux, et la nourriture en général. Elle aime pas les choux de Bruxelles. Toujours accompagnée de Peko un axolotl préhistorique à caractère assez tranché. Même si leurs caractères sont à l'opposé les 2 amis ne peuvent pas se séparer."


def get_session_history(session_id):
    # S'il n''existe pas d'historique, on rajoute le premier message
    if len(SQLChatMessageHistory(session_id, "sqlite:///memory.db").get_messages()) == 0:
        SQLChatMessageHistory(session_id, "sqlite:///memory.db").add_message(SystemMessage(first_system_message))
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db") 

    

trimmer = trim_messages(
    max_tokens=2000,
    strategy="last",
    token_counter=llm,
    include_system=True,
    allow_partial=True,
)


runnable_with_history = RunnableWithMessageHistory(
    trimmer | llm,
    get_session_history,
)


def run(guild_id, message):
    max_chars_per_message = 1900

    ai_output = runnable_with_history.invoke(
        HumanMessage(message),
        {'configurable': {'session_id': guild_id}}
    )

    if ai_output is None:
        return None
    
    message = ai_output.content
    list_of_messages = []

    while len(message) > max_chars_per_message:
        list_of_messages.append(message[:max_chars_per_message])
        message = message[max_chars_per_message:]

    list_of_messages.append(message)

    return list_of_messages


    
