import React, { useState, useRef, useEffect } from 'react';
import { Send, Heart, Sparkles, Target, TrendingUp, Calendar, BookOpen, Smile } from 'lucide-react';

const LifeCoachAI = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: "Hello! I'm your personal life coach AI. I'm here to help you achieve your goals, build positive habits, and create the life you envision. What aspect of your life would you like to work on today?",
      timestamp: new Date().toLocaleTimeString(),
      options: [
        { text: "Goal Setting", icon: Target, color: "from-emerald-500 to-teal-600" },
        { text: "Habit Building", icon: TrendingUp, color: "from-purple-500 to-pink-600" },
        { text: "Wellness", icon: Heart, color: "from-red-500 to-orange-600" },
        { text: "Mindfulness", icon: Sparkles, color: "from-blue-500 to-indigo-600" }
      ]
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputText.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      content: inputText,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    // Simulate AI response delay
    setTimeout(() => {
      const responses = [
        {
          content: "That's a wonderful insight! Let's explore this further. I believe you have the strength to overcome this challenge. What small step could you take today to move forward?",
          options: [
            { text: "Create Action Plan", icon: Calendar, color: "from-green-500 to-emerald-600" },
            { text: "Daily Affirmation", icon: Heart, color: "from-pink-500 to-rose-600" },
            { text: "Reflection Exercise", icon: BookOpen, color: "from-blue-500 to-cyan-600" }
          ]
        },
        {
          content: "I can sense your motivation! Remember, every journey begins with a single step. You're already showing courage by reaching out. What would success look like for you?",
          options: [
            { text: "Visualize Goals", icon: Sparkles, color: "from-purple-500 to-violet-600" },
            { text: "Track Progress", icon: TrendingUp, color: "from-orange-500 to-amber-600" },
            { text: "Celebrate Wins", icon: Smile, color: "from-yellow-500 to-orange-600" }
          ]
        }
      ];

      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      
      const aiMessage = {
        id: messages.length + 2,
        type: 'ai',
        content: randomResponse.content,
        timestamp: new Date().toLocaleTimeString(),
        options: randomResponse.options
      };
      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const handleOptionClick = (option) => {
    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      content: `I'd like to work on: ${option.text}`,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    setTimeout(() => {
      const aiMessage = {
        id: messages.length + 2,
        type: 'ai',
        content: `Excellent choice! Let's focus on ${option.text.toLowerCase()}. I'll guide you through some personalized strategies that will help you build momentum and achieve lasting change.`,
        timestamp: new Date().toLocaleTimeString(),
        options: [
          { text: "Start Now", icon: Sparkles, color: "from-green-500 to-emerald-600" },
          { text: "Learn More", icon: BookOpen, color: "from-blue-500 to-indigo-600" },
          { text: "Set Reminder", icon: Calendar, color: "from-purple-500 to-pink-600" }
        ]
      };
      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 1200);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const examplePrompts = [
    "I want to build better morning routines",
    "Help me overcome procrastination",
    "I need motivation to exercise regularly",
    "How can I improve my confidence?"
  ];

  return (
    <div className="flex flex-col h-screen bg-black text-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-900 to-gray-800 border-b border-gray-800 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-gradient-to-r from-rose-500 to-purple-600 p-2 rounded-lg shadow-lg animate-pulse">
              <Heart className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-lg font-semibold bg-gradient-to-r from-rose-400 to-purple-400 bg-clip-text text-transparent">
                Life Coach AI Agent
              </h1>
              <p className="text-sm text-gray-400">Your personal transformation companion</p>
            </div>
          </div>
          
          {/* Fusion Header Buttons */}
          <div className="flex items-center space-x-3">
            <button className="px-4 py-2 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 text-sm font-medium">
              <Target className="w-4 h-4 inline mr-2" />
              Goals
            </button>
            <button className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 text-sm font-medium">
              <TrendingUp className="w-4 h-4 inline mr-2" />
              Progress
            </button>
            <button className="px-4 py-2 bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 text-sm font-medium">
              <Sparkles className="w-4 h-4 inline mr-2" />
              Insights
            </button>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex max-w-3xl ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'} space-x-3`}>
              {/* Avatar */}
              <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                message.type === 'user' 
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 ml-3 shadow-lg animate-pulse' 
                  : 'bg-gradient-to-r from-rose-500 to-purple-600 mr-3 shadow-lg animate-pulse'
              }`}>
                {message.type === 'user' ? (
                  <Smile className="w-5 h-5" />
                ) : (
                  <Heart className="w-5 h-5" />
                )}
              </div>

              {/* Message Content */}
              <div className={`flex-1 ${message.type === 'user' ? 'mr-3' : 'ml-3'}`}>
                <div className={`p-4 rounded-2xl shadow-lg transform transition-all duration-500 hover:scale-105 ${
                  message.type === 'user' 
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white animate-slideInRight' 
                    : 'bg-gradient-to-r from-gray-800 to-gray-700 text-gray-100 animate-slideInLeft border border-gray-600'
                }`}>
                  <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>
                  
                  {/* Options for AI messages */}
                  {message.type === 'ai' && message.options && (
                    <div className="mt-4 space-y-2">
                      <p className="text-sm text-gray-300 mb-3">Choose an option:</p>
                      <div className="grid grid-cols-1 gap-2">
                        {message.options.map((option, index) => {
                          const IconComponent = option.icon;
                          return (
                            <button
                              key={index}
                              onClick={() => handleOptionClick(option)}
                              className={`flex items-center space-x-3 p-3 bg-gradient-to-r ${option.color} hover:shadow-lg rounded-lg transition-all duration-300 transform hover:scale-105 text-sm font-medium`}
                            >
                              <IconComponent className="w-4 h-4" />
                              <span>{option.text}</span>
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </div>
                <p className="text-xs text-gray-400 mt-2">
                  {message.timestamp}
                </p>
              </div>
            </div>
          </div>
        ))}

        {/* Typing Indicator */}
        {isTyping && (
          <div className="flex justify-start">
            <div className="flex max-w-3xl space-x-3">
              <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-r from-rose-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg animate-pulse">
                <Heart className="w-5 h-5" />
              </div>
              <div className="bg-gradient-to-r from-gray-800 to-gray-700 p-4 rounded-2xl shadow-lg border border-gray-600">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gradient-to-r from-rose-500 to-purple-600 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gradient-to-r from-rose-500 to-purple-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gradient-to-r from-rose-500 to-purple-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Example Prompts */}
      {messages.length === 1 && (
        <div className="px-4 py-2">
          <p className="text-sm text-gray-400 mb-3 flex items-center">
            <Sparkles className="w-4 h-4 mr-2 text-purple-400" />
            Get started with these prompts:
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {examplePrompts.map((prompt, index) => (
              <button
                key={index}
                onClick={() => setInputText(prompt)}
                className="text-left p-4 bg-gradient-to-r from-gray-800 to-gray-700 hover:from-gray-700 hover:to-gray-600 rounded-xl text-sm text-gray-300 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl border border-gray-700 hover:border-gray-600"
              >
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-gradient-to-r from-rose-500 to-purple-600 rounded-full animate-pulse"></div>
                  <span>{prompt}</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t border-gray-800 p-4 bg-gradient-to-r from-gray-900 to-gray-800">
        <div className="max-w-4xl mx-auto">
          <div className="relative flex items-end space-x-3">
            <div className="flex-1 relative">
              <textarea
                ref={inputRef}
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Share what's on your mind... I'm here to help you grow and thrive! 🌟"
                className="w-full bg-gradient-to-r from-gray-800 to-gray-700 text-white p-4 pr-12 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 border border-gray-600 shadow-lg placeholder-gray-400"
                rows="1"
                style={{ minHeight: '52px', maxHeight: '120px' }}
              />
            </div>
            <button
              onClick={handleSend}
              disabled={!inputText.trim() || isTyping}
              className="bg-gradient-to-r from-rose-500 to-purple-600 hover:from-rose-600 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-500 disabled:cursor-not-allowed p-4 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-3 text-center flex items-center justify-center">
            <Heart className="w-3 h-3 mr-1 text-rose-400" />
            Your AI life coach is here to support your personal growth journey
          </p>
        </div>
      </div>

      <style jsx>{`
        @keyframes slideInLeft {
          from {
            opacity: 0;
            transform: translateX(-20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }
        
        @keyframes slideInRight {
          from {
            opacity: 0;
            transform: translateX(20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }
        
        .animate-slideInLeft {
          animation: slideInLeft 0.5s ease-out;
        }
        
        .animate-slideInRight {
          animation: slideInRight 0.5s ease-out;
        }
      `}</style>
    </div>
  );
};

export default LifeCoachAI;
