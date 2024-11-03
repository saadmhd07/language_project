# Language Project
This project is a Streamlit web application that provides two main functionalities: Chat Conversation and Natural Conversation (Audio Conversation).

## Features

- **Chat Conversation**: A page for text-based chat interactions.
- **Natural Conversation**: A page for audio-based conversations.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    ```
2. Install Poetry if you haven't already:
    ```sh
    pip install poetry
    ```
3. Install the dependencies using Poetry:
    ```sh
    poetry install
    ```
4. Activate the virtual environment:
    ```sh
    poetry shell
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run streamlit_main.py
    ```
2. Open your web browser and navigate to [http://localhost:8501](http://localhost:8501).

## Project Structure

- `streamlit_main.py`: The main entry point of the application.
- `app_pages/`: Directory containing the different page modules.
  - `audio_conversation.py`: Module for the audio conversation page.
  - `chat_page.py`: Module for the chat conversation page.

## Configuration

The Streamlit application is configured in `streamlit_main.py`:

- **Page title**: "Langue Project"
- **Layout**: Wide

## Contributing

1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature-branch
    ```
3. Make your changes.
4. Commit your changes:
    ```sh
    git commit -m 'Add some feature'
    ```
5. Push to the branch:
    ```sh
    git push origin feature-branch
    ```
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Streamlit for providing the framework for building the web application.