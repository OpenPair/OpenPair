import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Sparkles } from 'lucide-react';
import '.././styles/main.scss';
import api from '../../hooks/api'

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      content: input.trim(),
      role: 'user',
      timestamp: new Date(),
    };

    console.log('Adding user message:', userMessage);
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      const response = await api.post('/api/query-client/', {
        message: input.trim(),
      });

      console.log('Full API Response:', response.data);

      // Check if response.data is an array
      if (!Array.isArray(response.data)) {
        console.error('Expected array response, got:', typeof response.data);
        throw new Error('Invalid response format');
      }

      // Convert all messages from the API to our frontend format
      const formattedMessages = response.data
        .sort((a, b) => a.created_at - b.created_at) // Sort by creation time, oldest first
        .map(msg => ({
          id: msg.id,
          content: msg.content[0].text.value,
          role: msg.role,
          timestamp: new Date(msg.created_at * 1000),
          vocab: msg.vocab || []
        }));

      // Update the messages state with the full conversation history
      setMessages(formattedMessages);
      
    } catch (error) {
      console.error('Error details:', error);

      const errorMessage = {
        id: (Date.now() + 1).toString(),
        content: "Sorry, there was an error processing your request. Please try again later.",
        role: 'assistant',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }

  console.log('Current messages state:', messages);

  return (
    <div className="app">
      <header className="header">
        <div className="header__container">
          <div className="header__logo">
            <Sparkles size={24} />
          </div>
          <div>
            <h1 className="header__title">AI Assistant</h1>
            <p className="header__subtitle">Powered by RAG Technology</p>
          </div>
        </div>
      </header>

      <div className="messages">
        <div className="messages__container">
          {messages.length === 0 && (
            <div className="message">
              <div className="message__content message__content--assistant">
                <p className="message__text">Hello! How can I help you today?</p>
              </div>
            </div>
          )}
          {messages.map((message, index) => {
            console.log('Rendering message:', message);
            return (
              <div
                key={`${message.id}-${index}`}
                className={`message ${message.role === 'user' ? 'message--user' : ''}`}
              >
                <div className="message__avatar">
                  {message.role === 'assistant' ? (
                    <Bot size={24} />
                  ) : (
                    <User size={24} />
                  )}
                </div>
                <div className={`message__content message__content--${message.role}`}>
                  <p className="message__text">{message.content}</p>
                  {message.vocab && message.vocab.length > 0 && (
                    <div className="message__vocab">
                      <h4 className="message__vocab-title">Key Terms:</h4>
                      <ul className="message__vocab-list">
                        {message.vocab.map((term) => (
                          <li key={term.id} className="message__vocab-item">
                            <strong>{term.word}</strong>: {term.definition}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  <span className="message__time">
                    {message.timestamp.toLocaleTimeString([], { 
                      hour: '2-digit', 
                      minute: '2-digit'
                    })}
                  </span>
                </div>
              </div>
            );
          })}
          {isLoading && (
            <div className="message">
              <div className="message__avatar">
                <Bot size={24} />
              </div>
              <div className="message__content message__content--assistant">
                <div className="message__text">
                  <Loader2 className="animate-spin" size={16} />
                  <span>AI is thinking...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="input-form">
        <form onSubmit={handleSubmit} className="input-form__container">
          <div className="input-form__group">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="input-form__field"
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="input-form__button"
            >
              <Send size={20} />
              <span>Send</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Chat;