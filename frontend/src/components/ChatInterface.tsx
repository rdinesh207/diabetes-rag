
import { useState } from 'react';
import { Send, User, Bot, Copy, ThumbsUp, ThumbsDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from '@/components/ui/select';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: Array<{
    title: string;
    journal: string;
    url: string;
    relevance: number;
  }>;
}

export const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: "Hello! I'm your AI research assistant specialized in diabetes research. I can help you find information from peer-reviewed medical publications. What would you like to know?",
      timestamp: new Date(),
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [model, setModel] = useState<'llm' | 'gemini'>('llm');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: input, model }),
      });
      if (!response.ok) throw new Error('Failed to fetch answer');
      const data = await response.json();
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: data.answer,
        timestamp: new Date(),
        sources: Array.isArray(data.citations)
          ? data.citations.map((citation: any) => ({
              title: citation.title || 'Unknown Title',
              journal: citation.journal || '',
              url: citation.url || '#',
              relevance: citation.relevance || 0.8,
            }))
          : undefined,
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.log(error);
      setMessages(prev => [
        ...prev,
        {
          id: (Date.now() + 2).toString(),
          type: 'assistant',
          content: 'Sorry, there was an error fetching the answer. Please try again.',
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-96">
      <ScrollArea className="flex-1 p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex gap-3 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`flex gap-3 max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                message.type === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white'
              }`}>
                {message.type === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>
              
              <div className="space-y-2">
                <div className={`rounded-2xl px-4 py-3 ${
                  message.type === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}>
                  <p className="text-sm">{message.content}</p>
                </div>
                
                {message.sources && (
                  <div className="space-y-2">
                    <p className="text-xs text-gray-500 font-medium">Sources:</p>
                    {message.sources.map((source, index) => (
                      <div key={index} className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h4 className="font-medium text-sm text-blue-900">{source.title}</h4>
                            <p className="text-xs text-blue-700 mt-1">{source.journal}</p>
                          </div>
                          <Badge variant="secondary" className="ml-2 text-xs">
                            {Math.round(source.relevance * 100)}% match
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                
                {message.type === 'assistant' && (
                  <div className="flex items-center gap-2 pt-1">
                    <Button variant="ghost" size="sm" className="h-6 px-2 text-xs">
                      <Copy className="w-3 h-3 mr-1" />
                      Copy
                    </Button>
                    <Button variant="ghost" size="sm" className="h-6 px-2 text-xs">
                      <ThumbsUp className="w-3 h-3" />
                    </Button>
                    <Button variant="ghost" size="sm" className="h-6 px-2 text-xs">
                      <ThumbsDown className="w-3 h-3" />
                    </Button>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 text-white flex items-center justify-center">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-gray-100 rounded-2xl px-4 py-3">
              <div className="flex items-center gap-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
      </ScrollArea>
      
      <div className="border-t p-4">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Select value={model} onValueChange={v => setModel(v as 'llm' | 'gemini')}>
            <SelectTrigger className="w-28" aria-label="Choose model" id="model-select" name="model">
              <SelectValue placeholder="Choose model" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="llm">LLM</SelectItem>
              <SelectItem value="gemini">Gemini</SelectItem>
            </SelectContent>
          </Select>
          <Input
            id="chat-input"
            name="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about diabetes research..."
            className="flex-1"
            disabled={isLoading}
          />
          <Button type="submit" disabled={isLoading || !input.trim()}>
            <Send className="w-4 h-4" />
          </Button>
        </form>
      </div>
    </div>
  );
};
