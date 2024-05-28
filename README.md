# AI Calendar Assistant

Experience seamless scheduling and human-like interaction with our AI Calendar Assistant, your ultimate tool to organize and navigate your daily events with a touch of artificial intuition.

## Technologies Used
- **Flask**: A micro web framework written in Python for the backend.
- **React**: A JavaScript library for building user interfaces, serving the front end.
- **OpenAI API**: Provides AI-powered responses and interactive capabilities.
- **SQLite**: A C-language library that implements a small, fast, self-contained, high-reliability, full-featured SQL database engine.

## Problem Statement
Modern-day people are swamped with numerous events and appointments. Our AI Calendar Assistant is designed to simplify the process of event management and offer an intuitive chat interface to manage your calendar easily. The goal is to improve productivity and time management through direct, conversational interaction.

## How to Run
To get the AI Calendar Assistant up and running, please follow these steps:

1. Ensure that you have Python and Node.js installed on your machine.
2. Clone the repository to your local machine.
3. Install the backend dependencies by navigating to the project root and running `pip install -r requirements.txt`.
4. Initialize the database with the provided scripts.
5. Start the backend server by running `python app.py`.
6. In a separate terminal window, navigate to the frontend directory and install the node modules using `npm install`.
7. Launch the frontend by running `npm start`.
8. Open your web browser and navigate to `http://localhost:3000` to view the application.

## Reflections
Building this project was a rewarding journey, as it allowed for the integration of multiple technologies and the exploration of how AI can be used in everyday applications to enhance efficiency and user experience.

## What I Learned
- How to incorporate AI services with OpenAI to handle complex user queries.
- Improved understanding of full-stack development and communication between frontend and backend.
- Advanced React pattern usage, state management, and functional component architecture.

## Challenges and Solutions
One of the challenges faced was ensuring that the AI responses were contextually relevant and integrated seamlessly with the event creation process. To address this, a robust backend logic was implemented to parse AI responses and trigger the appropriate actions within the application.

Another difficulty was managing dates and times across different components and ensuring consistent format parsing. Utilizing libraries like React DatePicker helped to standardize date handling across the application.

## Conclusion
This project demonstrates a practical application of AI within a web-based calendar system, emphasizing user interactivity, convenience, and efficiency in personal scheduling. It has laid a foundation for future projects that aim to bring more intelligent features to help with daily productivity.