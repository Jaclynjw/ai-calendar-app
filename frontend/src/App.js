import React, { useEffect, useState } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import Modal from 'react-modal';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import axios from 'axios';
import './App.css';

Modal.setAppElement('#root');

function App() {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [eventTitle, setEventTitle] = useState('');
  const [startTime, setStartTime] = useState(new Date());
  const [endTime, setEndTime] = useState(new Date());
  const [location, setLocation] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('Meeting');
  const [chatHistory, setChatHistory] = useState([]);
  const [inputText, setInputText] = useState('');
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [eventDetailModalIsOpen, setEventDetailModalIsOpen] = useState(false);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await axios.get('/api/events');
      const formattedEvents = response.data.map(event => ({
        title: event.title,
        start: new Date(event.start_time),
        end: new Date(event.end_time),
        extendedProps: {
          location: event.location,
          description: event.description,
          category: event.category
        }
      }));
      setEvents(formattedEvents);
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  };

  const handleFileChange = (event) => {
    // Implementation for file change event
  };

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSubmit = async () => {
    if (!inputText.trim()) {
      return; // Prevent empty messages from being sent
    }

    // Add user's message to chat history
    const userMessage = {
      role: 'user',
      message: inputText
    };
    setChatHistory(currentChatHistory => [...currentChatHistory, userMessage]);
    setInputText(''); // Clear the input field

    try {
      const response = await axios.post('/api/chat', { message: inputText });
      const aiMessage = {
        role: 'ai',
        message: response.data.ai_message
      };
      // Add AI's response to chat history
      setChatHistory(currentChatHistory => {
        const newChatHistory = [...currentChatHistory, aiMessage];
        fetchEvents(); // Refresh the calendar after receiving the AI message
        return newChatHistory;
      });
    } catch (error) {
      console.error('Chat API error:', error);
      setChatHistory(currentChatHistory => {
        const newChatHistory = [...currentChatHistory, {
          role: 'ai',
          message: 'Sorry, I encountered an error. Please try again.'
        }];
        fetchEvents(); // Refresh the calendar even if there's an error
        return newChatHistory;
      });
    }
  };

  const handleSubmitEvent = async () => {
    if (!eventTitle || !startTime || !endTime) {
      alert('Please fill in all required fields.');
      return;
    }
    if (startTime >= endTime) {
      alert('Start time must be before end time.');
      return;
    }

    const event = {
      title: eventTitle,
      start_time: startTime,
      end_time: endTime,
      location: location,
      description: description,
      category: category
    };

    try {
      const response = await axios.post('/api/events', event);
      if (response.status === 201) {
        alert('Event created successfully!');
        setModalIsOpen(false);
        fetchEvents();
      } else {
        alert('Failed to create event.');
      }
    } catch (error) {
      console.error('Error creating event:', error);
      alert('Error creating event. Please try again.');
    }
  };

  const handleEventClick = (clickInfo) => {
    setSelectedEvent(clickInfo.event);
    setEventDetailModalIsOpen(true);
  };

  return (
    <div className="app-container">
      <div className="calendar-container">
        <button onClick={() => setModalIsOpen(true)} className="create-event-button">
          Create Event
        </button>
        <FullCalendar
          plugins={[dayGridPlugin]}
          initialView="dayGridMonth"
          events={events}
          eventClick={handleEventClick}
        />
      </div>
      <Modal isOpen={modalIsOpen} onRequestClose={() => setModalIsOpen(false)} style={customStyles}>
        <div className="modal-header">
          <h2>Add event</h2>
          <button onClick={() => setModalIsOpen(false)} className="close-modal-button">X</button>
        </div>
        <form onSubmit={(e) => e.preventDefault()} className="event-form">
          <div className="form-group">
            <label>
              <i className="fas fa-calendar-alt"></i> Event Title:
              <input
                type="text"
                value={eventTitle}
                onChange={e => setEventTitle(e.target.value)}
              />
            </label>
          </div>
          <div className="form-group">
            <div className="date-time-picker">
              <label htmlFor="start-time">Start Time:</label>
              <DatePicker
                id="start-time"
                selected={startTime}
                onChange={setStartTime}
                showTimeSelect
                dateFormat="Pp"
                timeIntervals={15}
                required
              />
            </div>
            <div className="date-time-picker">
              <label htmlFor="end-time">End Time:</label>
              <DatePicker
                id="end-time"
                selected={endTime}
                onChange={setEndTime}
                showTimeSelect
                dateFormat="Pp"
                timeIntervals={15}
                required
              />
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="location">Location:</label>
            <input
              id="location"
              type="text"
              value={location}
              onChange={e => setLocation(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="description">Description:</label>
            <textarea
              id="description"
              value={description}
              onChange={e => setDescription(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="category">Category:</label>
            <select
              id="category"
              value={category}
              onChange={e => setCategory(e.target.value)}
              required
            >
              <option value="Meeting">Meeting</option>
              <option value="Workshop">Workshop</option>
              <option value="Personal">Personal</option>
              {/* Add more options as needed */}
            </select>
          </div>
          <div className="form-group">
            <button type="button" onClick={handleSubmitEvent} className="submit-event-button">Save</button>
          </div>
        </form>
      </Modal>
      {selectedEvent && (
        <Modal isOpen={eventDetailModalIsOpen} onRequestClose={() => setEventDetailModalIsOpen(false)} style={customStyles}>
          <div className="modal-header">
            <h2>Event Details</h2>
            <button onClick={() => setEventDetailModalIsOpen(false)} className="close-modal-button">X</button>
          </div>
          <div className="event-details">
            <h3>{selectedEvent.title}</h3>
            <p><strong>Start:</strong> {selectedEvent.start.toLocaleString()}</p>
            <p><strong>End:</strong> {selectedEvent.end.toLocaleString()}</p>
            <p><strong>Location:</strong> {selectedEvent.extendedProps.location}</p>
            <p><strong>Description:</strong> {selectedEvent.extendedProps.description}</p>
            <p><strong>Category:</strong> {selectedEvent.extendedProps.category}</p>
          </div>
        </Modal>
      )}
      <div className="conversation-container">
        <div className="chat-history">
          {chatHistory.map((chat, index) => (
            <div
              key={index}
              className={`chat-message ${chat.role === 'user' ? 'user' : 'ai'}`}
            >
              {chat.message}
            </div>
          ))}
        </div>
        <div className="input-container">
          <label htmlFor="file-upload" className="file-upload-btn">
            <i className="fas fa-paperclip"></i>
          </label>
          <input
            id="file-upload"
            type="file"
            onChange={handleFileChange}
            className="file-input"
          />
          <input
            type="text"
            value={inputText}
            onChange={handleInputChange}
            placeholder="Type your message..."
            className="text-input"
          />
          <button onClick={handleSubmit} className="send-button">
            <i className="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;

// Styles for the modal to ensure it appears over a slightly grayed-out background
const customStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    transform: 'translate(-50%, -50%)',
    zIndex: '1000', // Ensure the modal is above everything else
  },
  overlay: {
    backgroundColor: 'rgba(0, 0, 0, 0.5)', // Darken the background
  },
};
