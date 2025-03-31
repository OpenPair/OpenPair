import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Sparkles } from 'lucide-react';
import '.././styles/main.scss';
import api from '../../hooks/api'

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    const stored = localStorage.getItem("chat_history");
    if(stored){
      try {
        const parsed = JSON.parse(stored);
        const messagesWithDates = parsed.map(msg => ({
          ...msg,
          timestamp: new Date(msg.timestamp)
        }));
        setMessages(messagesWithDates);
        setIsFetching(false);
      } catch(err) {
        console.error("Failed to parse local chat: ", err);
      }
    }
    setIsFetching(false);
  }, []);

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

    setIsLoading(true);
    
    try {
      const response = await api.post('/api/query-client/', {
        message: input.trim(),
      });

      console.log('=== Frontend Timestamp Debug ===');
      console.log('API Response:', response.data);
      console.log('Response timestamps:', response.data.map(msg => ({
        role: msg.role,
        unix_timestamp: msg.timestamp,
        js_date: new Date(msg.timestamp * 1000),
        readable: new Date(msg.timestamp * 1000).toLocaleString()
      })));

      if (!Array.isArray(response.data)) {
        throw new Error('Invalid response format');
      }

      // Add new messages to existing messages
      setMessages(prevMessages => {
        // Convert Unix timestamps to JavaScript Date objects
        const formattedNewMessages = response.data.map(msg => {
          const jsDate = new Date(msg.timestamp * 1000);
          console.log(`Converting message timestamp:`, {
            role: msg.role,
            unix_timestamp: msg.timestamp,
            as_date: jsDate.toLocaleString()
          });
          return {
            ...msg,
            timestamp: jsDate  // Convert Unix timestamp to Date object
          };
        });
        
        const newMessages = [...prevMessages, ...formattedNewMessages];
        localStorage.setItem("chat_history", JSON.stringify(newMessages));
        return newMessages;
      });
      
    } catch (error) {
      console.error('Error:', error);
      // Handle error appropriately - maybe show a user-friendly message
    } finally {
      setInput('');  
      setIsLoading(false);
    }
  }

  const handleClearChat = async () => {
    setMessages([]);
    localStorage.removeItem("chat_history");
  };

  const shouldShowTimestamp = (currentMsg, prevMsg) => {
    if (!prevMsg) return true;
    
    if (!(currentMsg.timestamp instanceof Date)) {
      console.warn('Invalid timestamp for message:', {
        role: currentMsg.role,
        timestamp: currentMsg.timestamp
      });
      return true;
    }
    
    const timeDiff = currentMsg.timestamp - prevMsg.timestamp;
    const fiveMinutes = 5 * 60 * 1000;
    return timeDiff > fiveMinutes || currentMsg.role !== prevMsg.role;
  };

  if (isFetching) {
    return (
      <div className="app">
        <div className="loading-screen">
          <Loader2 className="animate-spin" size={32} />
          <p>Loading chat history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-container">
      <header className="header">
        <div className="header__container">
          <div className="header__logo">
            <Sparkles size={24} />
          </div>
          <div className="header__content">
            <h1 className="header__title">AI Assistant</h1>
            <p className="header__subtitle">Powered by RAG Technology</p>
          </div>
          <button 
            onClick={handleClearChat}
            className="header__clear-button"
            title="Clear chat history"
          >
            Clear Chat
          </button>
        </div>
      </header>

      <main className="chat-main">
        <div className="messages">
          <div className="messages__container">
            {messages.length === 0 ? (
              <div className="message message--welcome">
                <div className="message__content message__content--assistant">
                  <div className="message__avatar">
                    <Bot size={24} />
                  </div>
                  <div className="message__bubble">
                    <p className="message__text">Hello! How can I help you today?</p>
                  </div>
                </div>
              </div>
            ) : (
              messages.map((message, index) => {
                const prevMessage = index > 0 ? messages[index - 1] : null;
                const showTimestamp = shouldShowTimestamp(message, prevMessage);
                const isFirstInGroup = !prevMessage || prevMessage.role !== message.role;
                
                return (
                  <div
                    key={`${message.id}-${index}`}
                    className={`
                      message 
                      ${message.role === 'user' ? 'message--user' : ''} 
                      ${isFirstInGroup ? 'message--group-start' : 'message--group-item'}
                    `}
                  >
                    {isFirstInGroup && (
                      <div className="message__avatar">
                        {message.role === 'assistant' ? (
                          <Bot size={24} />
                        ) : (
                          <User size={24} />
                        )}
                      </div>
                    )}
                    <div className={`message__content message__content--${message.role}`}>
                      <div className="message__bubble">
                        <p className="message__text">
                          {message.content}
                        </p>
                      </div>
                      {showTimestamp && (
                        <span className="message__time">
                          {message.timestamp.toLocaleDateString([], {
                            month: 'numeric',
                            day: 'numeric'
                          })} {message.timestamp.toLocaleTimeString([], { 
                            hour: '2-digit', 
                            minute: '2-digit'
                          })}
                        </span>
                      )}
                    </div>
                  </div>
                );
              })
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </main>

      <footer className="chat-footer">
        <form onSubmit={handleSubmit} className="input-form">
          <div className="input-form__container">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="input-form__field"
              disabled={isLoading}
            />
            <button 
              type="submit" 
              className="input-form__button"
              disabled={isLoading || !input.trim()}
            >
              {isLoading ? <Loader2 className="animate-spin" size={24} /> : <Send size={24} />}
            </button>
          </div>
        </form>
      </footer>
    </div>
  );
}

export default Chat;