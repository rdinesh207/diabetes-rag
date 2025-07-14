
import { ChatInterface } from '@/components/ChatInterface';

export default function Index() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-white to-blue-50 p-6 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-4 text-center">🧬 PubMed GenAI RAG Chat</h1>
      <div className="w-full max-w-3xl mb-8">
        <ChatInterface />
      </div>
    </div>
  );
}
