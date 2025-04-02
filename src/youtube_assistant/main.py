import traceback
import streamlit as st
from src.youtube_assistant.ui.streamlit import StreamlitUILoader
from src.youtube_assistant.llm import get_llm
from src.youtube_assistant.graph import GraphBuilder
from src.youtube_assistant.ui.streamlit import DisplayResultStreamlit



def youtube_assistant():
    ui = StreamlitUILoader()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    with st.form("YouTube Assistant"):
        youtube_url = st.text_input(label="Enter the YouTube URL", placeholder="YouTube URL")
        submit = st.form_submit_button("Submit")
        

    if submit:
        try:

            llm = get_llm(user_input=user_input)
            if not llm:
                st.error("Error: LLM model could not be initialized.")
                return
            
            usecase = user_input['selected_usecase']
            if not usecase:
                st.error("Error: No use case selected.")
                return
            
            if user_input['selected_llm'] == "Anthropic":
                selected_llm_model = user_input['selected_anthropic_model']
            elif user_input['selected_llm'] == "OpenAI":
                selected_llm_model = user_input['selected_openai_model']
            elif user_input['selected_llm'] == "Groq":
                selected_llm_model = user_input['selected_groq_model']
            

            try:

                # if ('selected_usecase' not in st.session_state or 
                #     'selected_llm_name' not in st.session_state or 
                #     'selecetd_llm_model_model' not in st.session_state):

                #     st.session_state['selected_usecase'] = usecase
                #     st.session_state['selected_llm_name'] = type(llm).__name__
                #     st.session_state['selected_llm_model_name'] = selected_llm_model
                #     graph = GraphBuilder(user_input).setup_graph()
                #     st.session_state['graph'] = graph
                #     st.info("Creating new Graph") #
                #     st.code(user_input) # 
                # else:
                #     if (
                #         st.session_state['selected_usecase'] != usecase or
                #         st.session_state['selected_llm_name'] != type(llm).__name__ or
                #         st.session_state['selected_llm_model_name'] != selected_llm_model
                #     ):
                #         st.info("Creating new Graph with updates") # 
                #         st.code(user_input) # 
                #         st.session_state['selected_usecase'] = usecase
                #         st.session_state['selected_llm_name'] = type(llm).__name__
                #         st.session_state['selected_llm_model_name'] = selected_llm_model
                #         graph = GraphBuilder(user_input).setup_graph()
                #         st.session_state['graph'] = graph
                #     else:
                #         st.info("No changes in the graph")
                
                # graph = st.session_state['graph']
                
                graph = GraphBuilder(user_input).setup_graph()
                if graph is None:
                    st.error("Error: Graph setup failed.")
                    return
                
                DisplayResultStreamlit(usecase, graph, youtube_url).display_result_on_ui()

            except Exception as e:
                st.error(f"Error: {e}\n\{traceback.format_exc()}")

        except Exception as e:
            st.error(f"Error: {e}\n\{traceback.format_exc()}")

    else:
        st.info("Provide the YouTube URL to continue.")