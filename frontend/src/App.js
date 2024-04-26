import React from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction'; // for draggable
import axios from 'axios';
import './App.css'; // Make sure you import the CSS file

class App extends React.Component {
  state = {
    chatHistory: [],
    inputText: '',
    selectedFile: null
  };

  // handle date click
  handleDateClick = (arg) => {
    alert('Date clicked: ' + arg.dateStr);
  };

  // handle file selection
  handleFileChange = event => {
    this.setState({ selectedFile: event.target.files[0] });
  };

  // handle input change
  handleInputChange = event => {
    this.setState({ inputText: event.target.value });
  };

  // handle form submit
  handleSubmit = async () => {
    const formData = new FormData();
    formData.append('file', this.state.selectedFile);
    formData.append('text', this.state.inputText);

    try {
      const response = await axios.post('/api/message', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      // Assuming your API returns the updated chat history
      this.setState({
        chatHistory: response.data.chatHistory,
        inputText: '',
        selectedFile: null
      });
    } catch (error) {
      console.error('Error submitting message:', error);
    }
  };

  render() {
    return (
      <div className="app-container">
        <div className="calendar-container">
          <FullCalendar
            plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
            initialView="dayGridMonth"
            editable={true}
            selectable={true}
            selectMirror={true}
            dayMaxEvents={true}
            weekends={true}
            dateClick={this.handleDateClick}
          />
        </div>
        <div className="conversation-container">
          <div className="chat-history">
            {this.state.chatHistory.map((chat, index) => (
              <div key={index} className="chat-message">{chat.message}</div>
            ))}
          </div>
          <div className="input-container">
            <label htmlFor="file-upload" className="file-upload-btn">
              <i className="fas fa-paperclip"></i>
            </label>
            <input
              id="file-upload"
              type="file"
              onChange={this.handleFileChange}
              className="file-input"
            />
            <input
              type="text"
              value={this.state.inputText}
              onChange={this.handleInputChange}
              placeholder="Type your message..."
              className="text-input"
            />
            <button onClick={this.handleSubmit} className="send-button">
              <i className="fas fa-paper-plane"></i>
            </button>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
