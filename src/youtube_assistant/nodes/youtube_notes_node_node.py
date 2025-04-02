import streamlit as st
import traceback
from typing import Dict, Optional
from src.youtube_assistant.llm import get_llm
from src.youtube_assistant.state import BlogState
from langchain_core.messages import SystemMessage, HumanMessage


class YouTubeNotesNode:
    """
    Node for generating structured learning notes from YouTube video transcripts.
    Creates comprehensive, well-organized notes ideal for review after watching a video.
    """
    
    def __init__(self, user_input: Dict[str, str]):
        """
        Initialize the YouTube notes generator.
        
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
        

    def _create_notes_messages(self, transcript: str) -> list:
        """
        Create the system and human messages for the notes generation LLM.
        
        Args:
            transcript (str): The validated transcript.
            
        Returns:
            list: A list of messages for the LLM.
        """
        system_msg = SystemMessage(
            content=(
                "You are an expert educational content creator specializing in transforming video lectures "
                "into comprehensive study notes. You excel at organizing information into clear, structured "
                "formats that optimize learning and retention.\n\n"
                
                "Guidelines for creating educational notes:\n"
                "1. Begin with a concise overview of the video's main topic and learning objectives\n"
                "2. Create a clear hierarchical structure with main topics and subtopics\n"
                "3. Use numbered sections for sequential concepts and bulleted lists for key points\n"
                "4. Include all important definitions, formulas, and terminology with clear explanations\n"
                "5. Highlight critical concepts, principles, and takeaways in each section\n"
                "6. Preserve examples, case studies, and practical applications from the video\n"
                "7. Include any mentioned references, resources, or further reading materials\n"
                "8. Add visual indicators (e.g., '*' or '→') for especially important concepts\n"
                "9. Format the notes for maximum readability and quick review\n"
                "10. End with a summary of key points to remember\n\n"
                
                "Your notes should be comprehensive enough to serve as a standalone study resource "
                "while being concise and well-structured for efficient revision. Format your notes using "
                "markdown with appropriate headings (# for main topics, ## for subtopics, etc.), "
                "bullet points, numbered lists, and emphasis where needed."
            )
        )
        
        human_msg = HumanMessage(
            content=(
                "Please transform this YouTube video transcript into professional, comprehensive study notes. "
                "These notes will be used by learners who have watched the video and need a structured resource "
                "for review and revision.\n\n"
                
                "For these study notes:\n"
                "- Create a clear hierarchical organization of topics and concepts\n"
                "- Include all key information, theories, methodologies, and important details\n"
                "- Format definitions, formulas, and important concepts for easy reference\n"
                "- Break down complex ideas into digestible components\n"
                "- Include any examples or applications mentioned\n"
                "- Use appropriate markdown formatting for structure (headings, lists, emphasis)\n"
                "- Create a notes structure that facilitates quick review and retention\n\n"
                
                f"Here is the transcript:\n\n{transcript}\n\n"
                
                "Please provide comprehensive study notes that would help a student effectively "
                "review and master the material covered in this video."
            )
        )
        
        return [system_msg, human_msg]
    
    def generate_youtube_notes_node(self, state: BlogState) -> Dict[str, str]:
        """
        Generate educational notes based on the transcript in the state.
        
        Args:
            state (BlogState): The application state containing the transcript.
            
        Returns:
            Dict[str, str]: A dictionary containing the generated educational notes.
            
        Raises:
            RuntimeError: If the notes generation process fails.
        """
        try:
            transcript = state.get("youtube_transcript")
            if not transcript:
                error_msg = "YouTube transcript is missing"
                st.error(error_msg)
                raise ValueError(error_msg)
            
            
            messages = self._create_notes_messages(transcript)
            
            try:
                notes_response = self.llm.invoke(
                    input=messages,
                )
                
                if not hasattr(notes_response, 'content'):
                    error_msg = "Unexpected response format from LLM"
                    st.error(error_msg)
                    raise ValueError(error_msg)
                
                notes_content = notes_response.content
                
                if not notes_content.strip():
                    error_msg = "Generated notes are empty"
                    st.error(error_msg)
                    raise ValueError(error_msg)
                
                return {'video_notes': notes_content}
                
            except Exception as e:
                error_msg = f"Notes generation failed: {str(e)}"
                st.error(error_msg)
                st.code(traceback.format_exc(), language="python")
                raise RuntimeError(error_msg)
                
        except Exception as e:
            error_msg = f"YouTube notes generation process failed: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise RuntimeError(error_msg)