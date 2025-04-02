import streamlit as st
import traceback
from typing import Dict, Optional
from src.youtube_assistant.llm import get_llm
from src.youtube_assistant.state import BlogState
from langchain_core.messages import SystemMessage, HumanMessage


class YouTubeSummarizerNode:
    """
    Node for generating professional summaries from YouTube video transcripts.
    Takes a transcript from the state and produces a concise, structured summary.
    """
    
    def __init__(self, user_input: Dict[str, str]):
        """
        Initialize the YouTube summarizer.
        
        Args:
            user_input (Dict[str, str]): User configuration for the LLM.
        """
        try:
            self.llm = get_llm(user_input)
        except Exception as e:
            error_msg = f"Failed to initialize LLM: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise RuntimeError(error_msg)
    
    
    def _create_summary_messages(self, transcript: str) -> list:
        """
        Create the system and human messages for the summarization LLM.
        
        Args:
            transcript (str): The validated transcript.
            
        Returns:
            list: A list of messages for the LLM.
        """
        system_msg = SystemMessage(
            content=(
                "You are an expert content summarizer specializing in creating concise, "
                "informative, and well-structured summaries from YouTube video transcripts. "
                "Your summaries capture the essence of the content while maintaining critical details and insights.\n\n"
                
                "Guidelines for summarization:\n"
                "1. Begin with an executive summary (2-3 sentences) capturing the main point\n"
                "2. Identify and include the 3-5 key points or arguments presented\n"
                "3. Preserve important statistics, data points, and expert quotes\n"
                "4. Maintain the original tone and perspective of the content\n"
                "5. Structure the summary with clear sections and logical flow\n"
                "6. Use bullet points for lists of features, benefits, or steps\n"
                "7. Include a brief conclusion with main takeaways\n"
                "8. Keep the summary to approximately 15-20% of the original length\n"
                "9. Focus on substance over repetition or filler content\n"
                "10. Write in a professional, clear, and objective tone\n\n"
                
                "Format your summary using markdown for better readability, with ## for section headings "
                "and bullet points where appropriate. Ensure the summary stands on its own as a "
                "complete, valuable document that conveys the essential information from the video."
            )
        )
        
        human_msg = HumanMessage(
            content=(
                "Please create a comprehensive summary of this YouTube video based on its transcript.\n\n"
                
                "In your summary:\n"
                "- Begin with a concise overview of what the video is about\n"
                "- Extract and highlight the main points, insights, and key takeaways\n"
                "- Organize information into logical sections with clear headings\n"
                "- Preserve important facts, figures, examples, and quotes\n"
                "- Conclude with the significance or implications of the content\n"
                "- Use markdown formatting for structure and readability\n\n"
                
                f"Here is the transcript:\n\n{transcript}\n\n"
                
                "Please provide a professional summary that would be valuable to someone "
                "who wants to understand the key content without watching the entire video."
            )
        )
        
        return [system_msg, human_msg]
    
    def generate_youtube_summary_node(self, state: BlogState) -> Dict[str, str]:
        """
        Generate a summary based on the transcript in the state.
        
        Args:
            state (BlogState): The application state containing the transcript.
            
        Returns:
            Dict[str, str]: A dictionary containing the generated summary.
            
        Raises:
            RuntimeError: If the summary generation process fails.
        """
        try:
            transcript = state.get("youtube_transcript")
            if not transcript:
                error_msg = "YouTube transcript is missing"
                st.error(error_msg)
                raise ValueError(error_msg)
            
            messages = self._create_summary_messages(transcript)
            
            st.info("Starting summary generation. This may take a moment...")
            
            try:
                with st.spinner("Generating summary..."):
                    summary_response = self.llm.invoke(
                        input=messages
                    )
                    
                    if not hasattr(summary_response, 'content'):
                        error_msg = "Unexpected response format from LLM"
                        st.error(error_msg)
                        raise ValueError(error_msg)
                    
                    summary_content = summary_response.content
                    
                    if not summary_content.strip():
                        error_msg = "Generated summary is empty"
                        st.error(error_msg)
                        raise ValueError(error_msg)

                    st.success("Summary generated successfully!")
                    
                    return {'video_summary': summary_content}
                
            except Exception as e:
                error_msg = f"Summary generation failed: {str(e)}"
                st.error(error_msg)
                st.code(traceback.format_exc(), language="python")
                raise RuntimeError(error_msg)
                
        except Exception as e:
            error_msg = f"YouTube summary generation process failed: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise RuntimeError(error_msg)