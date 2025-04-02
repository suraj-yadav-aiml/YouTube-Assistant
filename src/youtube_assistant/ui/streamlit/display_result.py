import streamlit as st
import traceback
from typing import Literal


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, youtube_url):
        self.usecase = usecase
        self.graph = graph
        self.youtube_url = youtube_url

        if "message_history" not in st.session_state:
            st.session_state.message_history = []   

    def _display_message(self, role: Literal["user", "assistant"], message: str) -> None:
        if role == "user":
            with st.chat_message(role):
                st.markdown(message)
        else:
            with st.chat_message(role):
                with st.expander(label="Generated blog", expanded=False):
                    st.markdown(message)
    
    def _display_chat_history(self) -> None:
        for chat in st.session_state.message_history:
            self._display_message(chat["role"], chat["message"])

    def handle_yt_blog_generation(self):
        self._display_chat_history()

        st.session_state.message_history.append({"role": "user", "message": self.youtube_url})
        self._display_message("user", self.youtube_url)

        try:
            with st.spinner("Generating blog..."):
                response = self.graph.invoke(
                    input= {
                        'youtube_url': self.youtube_url,
                    }
                )
                
            if 'final_blog' in response:
                ai_response = response['final_blog']
                
                st.session_state.message_history.append({"role": "assistant", "message": ai_response})
                self._display_message("assistant", ai_response)
                
                # Add download button for the blog
                st.download_button(
                    label="Download Blog as Markdown",
                    data=ai_response,
                    file_name="youtube_blog.md",
                    mime="text/markdown"
                )
            else:
                st.error("No blog content was generated.")

        except Exception as e:
            st.error(f"Error processing response: {str(e)}")
            st.code(traceback.format_exc(), language="python")
    
    def handle_yt_summarization(self):
        self._display_chat_history()

        st.session_state.message_history.append({"role": "user", "message": self.youtube_url})
        self._display_message("user", self.youtube_url)

        try:
            with st.spinner("Generating summary of the video..."):
                response = self.graph.invoke(
                    input= {
                        'youtube_url': self.youtube_url,
                    }
                )
                
            if 'video_summary' in response:
                ai_response = response['video_summary']
                
                st.session_state.message_history.append({"role": "assistant", "message": ai_response})
                self._display_message("assistant", ai_response)
                
                # Add download button for the Summary
                st.download_button(
                    label="Download Video Summary as Markdown",
                    data=ai_response,
                    file_name="Video_Summary.md",
                    mime="text/markdown"
                )
            else:
                st.error("No summary was generated.")

        except Exception as e:
            st.error(f"Error processing response: {str(e)}")
            st.code(traceback.format_exc(), language="python")

    def handle_yt_notes_generation(self):
        self._display_chat_history()

        st.session_state.message_history.append({"role": "user", "message": self.youtube_url})
        self._display_message("user", self.youtube_url)

        try:
            with st.spinner("Generating notes of the video..."):
                response = self.graph.invoke(
                    input= {
                        'youtube_url': self.youtube_url,
                    }
                )
                
            if 'video_notes' in response:
                ai_response = response['video_notes']
                
                st.session_state.message_history.append({"role": "assistant", "message": ai_response})
                self._display_message("assistant", ai_response)
                
                # Add download button for the Summary
                st.download_button(
                    label="Download Notes as Markdown",
                    data=ai_response,
                    file_name="Video_notes.md",
                    mime="text/markdown"
                )
            else:
                st.error("No notes was generated.")

        except Exception as e:
            st.error(f"Error processing response: {str(e)}")
            st.code(traceback.format_exc(), language="python")
        
    def display_result_on_ui(self):
        usecase_options = {
            "YouTube Video Blog Generation": self.handle_yt_blog_generation,
            "YouTube Video Summarization": self.handle_yt_summarization,
            "YouTube Video Notes": self.handle_yt_notes_generation,
        }

        handler = usecase_options.get(self.usecase)
        if handler:
            handler()
        else:
            st.error(f"Unsupported usecase: {self.usecase}")
            st.info("Supported usecases: " + ", ".join(usecase_options.keys()))

