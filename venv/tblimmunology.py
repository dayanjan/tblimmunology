# Copyright 2025 Dayanjan S. Wijesinghe, Ashim Malhotra, Micah Buller, 
# Kunal Modi, and Karim Pajazetovic
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Blueprint for Constructing an AI-Based Patient Simulation to Enhance the Integration of Foundational and Clinical Sciences in Didactic Immunology in A US Doctor of Pharmacy Program: A Step-By-Step Prompt Engineering and Coding Toolkit 

This module implements the main application entry point for the Team-Based Learning 
simulation platform, handling UI rendering and user interactions.
"""


from openai import OpenAI
import streamlit as st
import os
from pathlib import Path
import logging
from typing import Optional, List, Dict
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai"]["api_key"])


class ConversationExporter:
    """Handles conversation export functionality"""

    @staticmethod
    def format_conversation(messages: List[Dict[str, str]]) -> str:
        """Format conversation history into readable text"""
        formatted_text = "Team Based Learning Conversation Export\n"
        formatted_text += "=" * 50 + "\n\n"

        for message in messages:
            role = message["role"].upper()
            content = message["content"]
            formatted_text += f"{role}:\n{content}\n\n"
            formatted_text += "-" * 50 + "\n\n"

        return formatted_text

    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp for filename"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")


class CostCalculator:
    """Handles token cost calculations for different models"""

    MODEL_COSTS = {
        "gpt-4o-2024-11-20": {
            "input_cost": 2.50 / 1_000_000,  # $2.50 per 1M input tokens
            "output_cost": 10.00 / 1_000_000  # $10.00 per 1M output tokens
        },
        "gpt-4o-mini-2024-07-18": {
            "input_cost": 0.150 / 1_000_000,  # $0.150 per 1M input tokens
            "output_cost": 0.150 / 1_000_000  # $0.150 per 1M output tokens
        }
    }

    @staticmethod
    def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """
        Calculate the total cost for a given model and token usage
        """
        if model not in CostCalculator.MODEL_COSTS:
            logger.error(f"Unknown model: {model}")
            return 0.0

        costs = CostCalculator.MODEL_COSTS[model]
        input_cost = prompt_tokens * costs["input_cost"]
        output_cost = completion_tokens * costs["output_cost"]

        return input_cost + output_cost


class AppState:
    """Manages application state and initialization"""

    @staticmethod
    def initialize_session_state():
        """Initialize all session state variables"""
        initial_states = {
            'messages': [],
            'total_cost': 0.0,
            'system_message': "",
            'conversation_history': [],
            'error_log': [],
            'last_update': datetime.now().isoformat(),
            'current_exercise': None,
            'show_save_dialog': False,
            'pending_exercise_change': None
        }

        for key, initial_value in initial_states.items():
            if key not in st.session_state:
                st.session_state[key] = initial_value


class UIComponents:
    """Manages UI components and styling"""

    @staticmethod
    def setup_page():
        """Configure page settings and styling"""
        st.set_page_config(
            page_title="TBL Immunology",
            page_icon="🤖",
            layout="wide"
        )

        st.markdown("""
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                .stTextArea textarea {font-size: 16px;}
                .stButton button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                }
                .error-message {
                    color: red;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid red;
                    border-radius: 5px;
                }
            </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_header():
        """Render the application header"""
        st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <h1>VCU School of Pharmacy</h1>
                <h3>Team Based Learning Assistant</h3>
            </div>
        """, unsafe_allow_html=True)


class FileHandler:
    """Handles file operations"""

    @staticmethod
    def get_text_files(directory: str) -> List[str]:
        """Get list of text files from directory"""
        try:
            directory_path = Path(directory)
            if not directory_path.exists():
                logger.warning(f"Directory {directory} not found")
                return []
            return [f.stem for f in directory_path.glob("*.txt")]
        except Exception as e:
            logger.error(f"Error reading directory {directory}: {str(e)}")
            return []

    @staticmethod
    def load_system_message(file_name: str) -> Optional[str]:
        """Load system message from file"""
        try:
            file_path = Path('systemmessages') / f"{file_name}.txt"
            if not file_path.exists():
                raise FileNotFoundError(f"System message file {file_name} not found")
            return file_path.read_text()
        except Exception as e:
            logger.error(f"Error loading system message: {str(e)}")
            return None


class ChatHandler:
    """Handles chat operations and API calls"""

    @staticmethod
    def generate_response(
            messages: List[Dict[str, str]],
            model: str = "gpt-4o-mini-2024-07-18"
    ) -> Optional[Dict]:
        """Generate response using OpenAI API"""
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7
            )
            return {
                'content': response.choices[0].message.content,
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens
            }
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return None


def main():
    """Main application function"""
    # Initialize application state
    AppState.initialize_session_state()

    # Setup UI
    UIComponents.setup_page()
    UIComponents.render_header()

    # Sidebar
    with st.sidebar:
        st.title("Exercise Settings")

        # Exercise selector
        text_files = FileHandler.get_text_files('systemmessages')

        def on_exercise_change():
            if (st.session_state.messages and
                    st.session_state.exercise_selector != st.session_state.current_exercise):
                st.session_state.show_save_dialog = True
                st.session_state.pending_exercise_change = st.session_state.exercise_selector
                st.rerun()

        selected_file = st.selectbox(
            "Choose The Exercise You Will Attempt Today:",
            options=text_files if text_files else ["No exercises available"],
            key="exercise_selector",
            on_change=on_exercise_change
        )

        # Handle exercise change confirmation
        if st.session_state.show_save_dialog:
            st.markdown("---")
            st.warning("Would you like to save the current conversation before changing exercises?")

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("Yes, Save"):
                    # Format and save conversation
                    conversation_text = ConversationExporter.format_conversation(st.session_state.messages)
                    timestamp = ConversationExporter.get_timestamp()
                    filename = f"conversation_export_{timestamp}.txt"

                    # Trigger download
                    st.download_button(
                        label="Download Conversation",
                        data=conversation_text,
                        file_name=filename,
                        mime="text/plain",
                        key="save_before_change"
                    )

                    # Clear conversation after saving
                    st.session_state.messages = []
                    st.session_state.total_cost = 0.0
                    st.session_state.current_exercise = st.session_state.pending_exercise_change
                    st.session_state.show_save_dialog = False
                    st.rerun()

            with col2:
                if st.button("No, Continue"):
                    # Clear conversation without saving
                    st.session_state.messages = []
                    st.session_state.total_cost = 0.0
                    st.session_state.current_exercise = st.session_state.pending_exercise_change
                    st.session_state.show_save_dialog = False
                    st.rerun()

            with col3:
                if st.button("Cancel"):
                    # Revert exercise selection
                    st.session_state.exercise_selector = st.session_state.current_exercise
                    st.session_state.show_save_dialog = False
                    st.rerun()

        st.markdown("---")

        # Model selector
        model_name = st.radio(
            "Choose a model:",
            ("gpt-4o-2024-11-20", "gpt-4o-mini-2024-07-18"),
            help="Select the AI model to use for generating responses"
        )

        # Cost tracking
        st.markdown("---")
        st.metric(
            "Total Cost",
            f"${st.session_state.total_cost:.5f}",
            help="Running total of API costs"
        )

        # Conversation Controls
        st.markdown("---")
        st.title("Conversation Controls")

        # Clear conversation
        if st.button("Clear Conversation", type="primary"):
            st.session_state.messages = []
            st.session_state.total_cost = 0.0
            st.rerun()

        # Save conversation
        if st.button("Save Conversation", type="secondary"):
            if st.session_state.messages:
                # Format conversation
                conversation_text = ConversationExporter.format_conversation(st.session_state.messages)

                # Generate filename with timestamp
                timestamp = ConversationExporter.get_timestamp()
                filename = f"conversation_export_{timestamp}.txt"

                # Create download button
                st.download_button(
                    label="Download Conversation",
                    data=conversation_text,
                    file_name=filename,
                    mime="text/plain"
                )
            else:
                st.warning("No conversation to save yet.")

    # Load system message
    if selected_file != "No exercises available":
        system_message = FileHandler.load_system_message(selected_file)
        if system_message:
            st.session_state.system_message = system_message
        else:
            st.error("Failed to load system message")

    # Chat interface
    chat_container = st.container()

    # Display message history
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Input area
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Prepare messages for API call
        messages = [{"role": "system", "content": st.session_state.system_message}] + st.session_state.messages

        # Generate response
        with st.spinner("Thinking..."):
            response = ChatHandler.generate_response(
                messages=messages,
                model=model_name
            )

            if response:
                # Calculate cost using the CostCalculator
                cost = CostCalculator.calculate_cost(
                    model=model_name,
                    prompt_tokens=response['prompt_tokens'],
                    completion_tokens=response['completion_tokens']
                )
                st.session_state.total_cost += cost

                # Add assistant response to state
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response['content']
                })

                # Force refresh
                st.rerun()
            else:
                st.error("Failed to generate response. Please try again.")


if __name__ == "__main__":
    main()
