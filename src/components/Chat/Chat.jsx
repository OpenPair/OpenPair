import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Sparkles, RefreshCw } from 'lucide-react';
import '.././styles/main.scss';
import api from '../../hooks/api'

function Chat() {
  // console.log()
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // const fetchChatHistory = async () => {
  //   try {
  //     const response = await api.get('/api/chat-history/');
  //     console.log('chat history response: ', response)
      
  //     if (!Array.isArray(response.data)) {
  //       console.error('Expected array response, got:', typeof response.data);
  //       return;
  //     }

  //     const formattedMessages = response.data
  //       .sort((a, b) => a.created_at - b.created_at)
  //       .map(msg => ({
  //         id: msg.id,
  //         content: msg.content[0].text.value,
  //         role: msg.role,
  //         timestamp: new Date(msg.created_at * 1000),
  //         vocab: msg.vocab || []
  //       }));

  //     setMessages(formattedMessages);
  //   } catch (error) {
  //     console.error('Error fetching chat history:', error);
  //   } finally {
  //     setIsFetching(false);
  //   }
  // };

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
      content: input.trim(),  // Simple string content for user messages
      role: 'user',
      timestamp: new Date(),
    };

    setIsLoading(true);
    
    try {
      const response = await api.post('/api/query-client/', {
        message: input.trim(),
      });

      console.log('Full API response: ', response.data);

      if (!Array.isArray(response.data)) {
        throw new Error('Invalid response format');
      }

      // Add new messages to existing messages
      setMessages(prevMessages => {
        // Convert timestamps in the new messages to Date objects
        const formattedNewMessages = response.data.map(msg => ({
          ...msg,
          timestamp: new Date(msg.created_at * 1000) // Convert Unix timestamp to Date
        }));
        
        const newMessages = [...prevMessages, ...formattedNewMessages];
        // Update localStorage with complete history
        localStorage.setItem("chat_history", JSON.stringify(newMessages));
        return newMessages;
      });
      
    } catch (error) {
      console.error('Error:', error);
      const current_time = Date.now();
      const errorMessage = {
        id: current_time.toString(),
        content: "Sorry, there was an error processing your request. Please try again later.",
        role: 'assistant',
        created_at: Math.floor(current_time / 1000),  // Convert to Unix timestamp
        timestamp: Math.floor(current_time / 1000)  // Convert to Unix timestamp
      };
      
      setMessages(prevMessages => {
        const newMessages = [...prevMessages, errorMessage];
        // Update localStorage with complete history
        localStorage.setItem("chat_history", JSON.stringify(newMessages));
        return newMessages;
      });
    } finally {
    setInput('');  // Clear input right away
      setIsLoading(false);
    }
  }

  const handleClearChat = async () => {
    setMessages([]);
    localStorage.removeItem("chat_history");
  };

  const shouldShowTimestamp = (currentMsg, prevMsg) => {
    if (!prevMsg) return true;
    
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
    <div className="app">
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
            <RefreshCw size={20} />
          </button>
        </div>
      </header>

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
              // Only filter exact welcome messages
              const welcomePattern = /^hello!?\s+how\s+can\s+i\s+help\s+you\s+today/i;
              if (welcomePattern.test(message.content)) {
                return null;
              }
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
                        {typeof message.content === 'string' ? message.content : JSON.stringify(message.content)}
                      </p>
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
          {isLoading && (
            <div className="message message--typing">
              <div className="message__avatar">
                <Bot size={24} />
              </div>
              <div className="message__content message__content--assistant">
                <div className="message__bubble message__bubble--typing">
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
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="input-form__button"
            >
              <Send size={20} />
              <span className="sr-only">Send</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Chat;