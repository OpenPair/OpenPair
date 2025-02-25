import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Sparkles } from 'lucide-react';
import './styles/main.scss';

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

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        content: "This is a simulated response. Replace this with your actual RAG implementation.",
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1000);
  };

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
          {messages.map((message) => (
            <div
              key={message.id}
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
                <span className="message__time">
                  {message.timestamp.toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit'
                  })}
                </span>
              </div>
            </div>
          ))}
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