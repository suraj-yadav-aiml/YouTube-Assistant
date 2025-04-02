
import streamlit as st
import traceback
from typing import Dict
from langgraph.graph import START, END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from src.youtube_assistant.state import BlogState
from src.youtube_assistant.nodes import (
    TranscriptNode,
    GenerateBlogTitleNode,
    GenerateBlogContentNode,
    BlogAggregatorNode,
    YouTubeSummarizerNode,
    YouTubeNotesNode
)


class GraphBuilder:
    """
    Builder class for creating workflow graphs for different YouTube video processing use cases.
    """
    
    def __init__(self, user_input: Dict[str, str]):
        """
        Initialize the GraphBuilder with user input configuration.
        
        Args:
            user_input (Dict[str, str]): User configuration including selected use case and LLM settings.
        """
        self.user_input = user_input
        self.workflow = StateGraph(BlogState)
        self.nodes_initialized = False
        
        # Validate user input
        self._validate_user_input()
    
    def _validate_user_input(self) -> None:
        """
        Validate the user input to ensure it contains required fields.
        
        Raises:
            ValueError: If required fields are missing or invalid.
        """
        try:
            if not self.user_input:
                error_msg = "User input configuration is missing"
                st.error(error_msg)
                raise ValueError(error_msg)
                
            if 'selected_usecase' not in self.user_input:
                error_msg = "Selected use case is missing from user input"
                st.error(error_msg)
                raise ValueError(error_msg)
                
            selected_usecase = self.user_input['selected_usecase']
            valid_usecases = [
                "YouTube Video Blog Generation",
                "YouTube Video Summarization",
                "YouTube Video Notes"
            ]
            
            if selected_usecase not in valid_usecases:
                error_msg = f"Invalid use case selected: {selected_usecase}. Valid options are: {', '.join(valid_usecases)}"
                st.error(error_msg)
                raise ValueError(error_msg)
                
        except Exception as e:
            error_msg = f"User input validation failed: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise ValueError(error_msg)
    
    def initialize_nodes(self) -> None:
        """
        Initialize all node objects based on the selected use case.
        """
        try:

            # Initialize common nodes
            self.get_transcript_node = TranscriptNode().get_transcript_node
            
            if self.user_input['selected_usecase'] == 'YouTube Video Blog Generation':

                self.generate_blog_title_node = GenerateBlogTitleNode(self.user_input).generate_blog_title_node
                self.generate_blog_content_node = GenerateBlogContentNode(self.user_input).generate_blog_content_node
                self.blog_aggregator_node = BlogAggregatorNode().aggregate_blog_node
            
            if self.user_input['selected_usecase'] == 'YouTube Video Summarization':
                self.youtube_summarizer_node = YouTubeSummarizerNode(self.user_input).generate_youtube_summary_node
            
            if self.user_input['selected_usecase'] == 'YouTube Video Notes':
                self.youtube_notes_node = YouTubeNotesNode(self.user_input).generate_youtube_notes_node
            
            self.nodes_initialized = True
            
        except Exception as e:
            error_msg = f"Failed to initialize nodes: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise RuntimeError(error_msg)
    
    def _build_yt_blog_generator_graph(self) -> None:
        """
        Build the workflow graph for YouTube Video Blog Generation use case.
        
        This creates a graph that:
        1. Extracts the transcript from a YouTube video
        2. Generates a blog title from the transcript
        3. Generates blog content from the transcript
        4. Aggregates the title and content into a final blog
        """
        try:
            if not self.nodes_initialized:
                self.initialize_nodes()
                
            # Add nodes to workflow
            self.workflow.add_node("get_transcript_node", self.get_transcript_node)
            self.workflow.add_node("generate_blog_title_node", self.generate_blog_title_node)
            self.workflow.add_node("generate_blog_content_node", self.generate_blog_content_node)
            self.workflow.add_node("blog_aggregator_node", self.blog_aggregator_node)
            
            # Define workflow connections
            self.workflow.add_edge(START, "get_transcript_node")
            self.workflow.add_edge("get_transcript_node", "generate_blog_title_node")
            self.workflow.add_edge("get_transcript_node", "generate_blog_content_node")
            self.workflow.add_edge("generate_blog_title_node", "blog_aggregator_node")
            self.workflow.add_edge("generate_blog_content_node", "blog_aggregator_node")
            self.workflow.add_edge("blog_aggregator_node", END)
            
        except Exception as e:
            error_msg = f"Failed to build blog generator graph: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise RuntimeError(error_msg)
    
    def _build_yt_notes_generation_graph(self) -> None:
        """
        Build the workflow graph for YouTube Video Notes Generation use case.
        """
        try:
            if not self.nodes_initialized:
                self.initialize_nodes()

            self.workflow.add_node("get_transcript_node", self.get_transcript_node)
            self.workflow.add_node("youtube_notes_node", self.youtube_notes_node)
            
            self.workflow.add_edge(START, "get_transcript_node")
            self.workflow.add_edge("get_transcript_node", "youtube_notes_node")
            self.workflow.add_edge("youtube_notes_node", END)
            
        except Exception as e:
            error_msg = f"Failed to build blog generator graph: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise RuntimeError(error_msg)
        
    def _build_yt_summarization_graph(self) -> None:
        """
        Build the workflow graph for YouTube Video Summarization use case.
        """
        try:
            if not self.nodes_initialized:
                self.initialize_nodes()

            self.workflow.add_node("get_transcript_node", self.get_transcript_node)
            self.workflow.add_node("youtube_summarizer_node", self.youtube_summarizer_node)
            
            self.workflow.add_edge(START, "get_transcript_node")
            self.workflow.add_edge("get_transcript_node", "youtube_summarizer_node")
            self.workflow.add_edge("youtube_summarizer_node", END)
            
        except Exception as e:
            error_msg = f"Failed to build blog generator graph: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise RuntimeError(error_msg)
    
    def setup_graph(self) -> CompiledStateGraph:
        """
        Set up and build the appropriate graph based on the selected use case.
        
        Returns:
            CompiledStateGraph: The compiled workflow graph ready for execution.
            
        Raises:
            RuntimeError: If the graph setup fails.
        """
        try:            
            usecase_mapping = {
                "YouTube Video Blog Generation": self._build_yt_blog_generator_graph,
                "YouTube Video Summarization": self._build_yt_summarization_graph,
                "YouTube Video Notes": self._build_yt_notes_generation_graph
            }
            
            selected_usecase = self.user_input['selected_usecase']
            
            build_graph = usecase_mapping.get(selected_usecase)
            
            if not build_graph:
                error_msg = f"No graph builder found for use case: {selected_usecase}"
                st.error(error_msg)
                raise ValueError(error_msg)
            
            build_graph()

            return self.workflow.compile()
            
        except NotImplementedError as e:
            st.warning(f"{str(e)}")

        except Exception as e:
            error_msg = f"Failed to set up graph: {str(e)}"
            st.error(error_msg)
            st.code(traceback.format_exc(), language="python")
            raise RuntimeError(error_msg)