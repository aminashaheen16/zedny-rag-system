import React, { useState, useRef, useEffect } from 'react';
import { Send, Menu, Paperclip, Mic, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { chatApi, type ChatResponse } from '../../api/chat';
import type { ChatMessage, Chat, EscalationData } from '../../types';
import { ChatSidebar } from './ChatSidebar';
import { MessageBubble } from './MessageBubble';

// Mock Data for Demo
const MOCK_CHATS: Chat[] = [
    { id: '1', title: 'Technical Support', lastMessage: 'Issue resolved', lastMessageAt: new Date().toISOString() }
];

const ChatInterface: React.FC = () => {
    // --- State ---
    const [messages, setMessages] = useState<ChatMessage[]>([
        {
            id: 'welcome',
            role: 'assistant',
            content: 'Hello! I am **Zedny**, your intelligent support assistant. How can I help you today?',
            timestamp: new Date(),
            type: 'text'
        }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [isListening, setIsListening] = useState(false);
    const [sessionId, setSessionId] = useState<string | undefined>(undefined);
    const [incidentState, setIncidentState] = useState<any>(null);
    const [voiceLang, setVoiceLang] = useState<'ar-EG' | 'en-US'>('ar-EG');

    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);

    // --- Effects ---
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, loading]);

    // --- Handlers ---

    // 1. Voice Input
    const handleVoiceInput = () => {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert('Your browser does not support voice input. Please use Chrome or Edge.');
            return;
        }

        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        const recognition = new SpeechRecognition();

        recognition.lang = voiceLang;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = () => setIsListening(true);
        recognition.onend = () => setIsListening(false);
        recognition.onerror = () => setIsListening(false);

        recognition.onresult = (event: any) => {
            const transcript = event.results[0][0].transcript;
            setInput(prev => (prev + ' ' + transcript).trim());
        };

        try {
            recognition.start();
        } catch (e) {
            console.error(e);
        }
    };

    // 2. Send Message
    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const userText = input.trim();
        setInput('');

        // Optimistic UI Update
        const userMsg: ChatMessage = {
            id: Date.now().toString(),
            role: 'user',
            content: userText,
            timestamp: new Date(),
            type: 'text'
        };
        setMessages(prev => [...prev, userMsg]);
        setLoading(true);

        try {
            // Detect Category (Simple Frontend Heuristic)
            let category = 'Tech';
            const lower = userText.toLowerCase();
            if (lower.includes('price') || lower.includes('cost')) category = 'Commercial';
            else if (lower.includes('video') || lower.includes('design')) category = 'Media';
            else if (lower.includes('course')) category = 'Content';

            const payload = {
                message: userText,
                session_id: sessionId,
                incident_state: incidentState,
                department: category
            };

            const response: ChatResponse = await chatApi.sendMessage(payload);

            // Sync State
            if (response.incident_state) {
                setIncidentState(response.incident_state);
                if (response.incident_state.session_id) setSessionId(response.incident_state.session_id);
            }

            // Simulate Streaming Typing Effect
            const fullText = response.answer;
            const aiMsgId = (Date.now() + 1).toString();

            // Initial Empty Message
            const aiMsg: ChatMessage = {
                id: aiMsgId,
                role: 'assistant',
                content: '',
                timestamp: new Date(),
                category: response.incident_state?.category || category,
                type: 'text'
            };
            setMessages(prev => [...prev, aiMsg]);
            setLoading(false); // Stop loading spinner, start typing

            let i = 0;
            const interval = setInterval(() => {
                setMessages(prev => prev.map(m =>
                    m.id === aiMsgId ? { ...m, content: fullText.substring(0, i + 1) } : m
                ));
                i++;
                if (i >= fullText.length) {
                    clearInterval(interval);

                    // Post-Response Triggers
                    if (response.action_required === 'show_escalation_form' || response.should_escalate) {
                        setTimeout(() => {
                            setMessages(prev => [...prev, {
                                id: Date.now().toString(),
                                role: 'assistant',
                                content: 'escalation_trigger',
                                timestamp: new Date(),
                                type: 'escalation_form'
                            }]);
                        }, 500);
                    }
                }
            }, 10); // Typing Speed

        } catch (error) {
            setMessages(prev => [...prev, {
                id: Date.now().toString(),
                role: 'system',
                content: '⚠️ Connection Error: Ensure backend is running on port 8000.',
                timestamp: new Date(),
                isError: true
            }]);
            setLoading(false);
        }
    };

    // 3. Escalation & Forms
    const handleFormSubmit = async (data: EscalationData) => {
        try {
            // Map frontend data to backend Schema (EscalationReport)
            const reportPayload = {
                category: incidentState?.category || "General",
                summary: data.description, // Matches 'summary' in backend
                user_email: data.email,    // Critical for email sending
                customerName: data.name,   // For auto-registering lead
                metadata: {
                    user_phone: data.phone,
                    company_name: data.companyName,
                    user_type: data.userType,
                    institution: data.institution,
                    job_title: data.jobTitle,
                    field_of_study: data.fieldOfStudy
                },
                history: messages.map(m => `${m.role.toUpperCase()}: ${m.content}`),
                assigned_to: "mohammedrawan653@gmail.com" // Explicitly requesting routing to this email
            };

            await chatApi.submitReport(reportPayload);

            setMessages(prev => [...prev, {
                id: Date.now().toString(),
                role: 'assistant',
                content: `Thank you, ${data.name}. Your request has been successfully escalated. A confirmation email has been sent to ${data.email}, and our specialist will contact you shortly.`,
                timestamp: new Date(),
                type: 'success'
            }]);

            // Trigger Rating
            setTimeout(() => {
                setMessages(prev => [...prev, {
                    id: Date.now().toString(),
                    role: 'assistant',
                    content: 'rating_trigger',
                    timestamp: new Date(),
                    type: 'rating'
                }]);
            }, 1000);

        } catch (error) {
            console.error("Failed to submit report:", error);
            setMessages(prev => [...prev, {
                id: Date.now().toString(),
                role: 'system',
                content: '⚠️ Failed to submit report. Please try again or contact support directly.',
                timestamp: new Date(),
                isError: true
            }]);
        }
    };

    // 4. Ratings
    const handleRate = async (rating: number) => {
        if (sessionId) {
            await chatApi.submitRating({ session_id: sessionId, rating });
        }
    };

    return (
        <div className="flex h-screen bg-hero-gradient text-slate-50 overflow-hidden font-sans relative">
            {/* Background Effects */}
            <div className="absolute inset-0 z-0 pointer-events-none overflow-hidden">
                <div className="absolute top-[-10%] right-[-10%] w-[600px] h-[600px] bg-indigo-900/20 rounded-full blur-[120px]" />
                <div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-purple-900/20 rounded-full blur-[120px]" />
            </div>

            {/* Mobile Sidebar Toggle */}
            <div className="md:hidden fixed top-4 left-4 z-50">
                <button
                    onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                    className="p-2 bg-[#0F172A]/80 backdrop-blur border border-white/10 rounded-lg shadow-lg"
                >
                    {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
                </button>
            </div>

            {/* Sidebar */}
            <ChatSidebar
                chats={MOCK_CHATS}
                activeChatId={'1'}
                onSelectChat={() => { }}
                onNewChat={() => {
                    setMessages([]);
                    setSessionId(undefined);
                    setIncidentState(null);
                }}
                isOpen={isSidebarOpen}
            />

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col relative w-full h-full z-10">
                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 scrollbar-thin scrollbar-thumb-indigo-500/20">
                    <AnimatePresence initial={false}>
                        {messages.map((msg) => (
                            <MessageBubble
                                key={msg.id}
                                message={msg}
                                lang={incidentState?.language || 'en'}
                                onFormSubmit={handleFormSubmit}
                                onRate={handleRate}
                            />
                        ))}
                    </AnimatePresence>

                    {loading && (
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-4 pl-2">
                            <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center animate-pulse">
                                <span className="w-2 h-2 bg-indigo-400 rounded-full" />
                            </div>
                            <span className="text-sm text-slate-500 py-1">Zedny AI is thinking...</span>
                        </motion.div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 md:p-6 bg-[#0f172a]/40 backdrop-blur-xl border-t border-white/5 shadow-[0_-10px_40px_rgba(0,0,0,0.3)]">
                    <div className="max-w-4xl mx-auto flex items-end gap-3 bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-2 shadow-glass ring-1 ring-white/5 focus-within:ring-indigo-400/50 focus-within:bg-white/10 transition-all duration-300">
                        <button className="p-3 text-slate-400 hover:text-white rounded-xl hover:bg-white/5 transition-colors">
                            <Paperclip size={20} />
                        </button>

                        <textarea
                            ref={inputRef}
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && !e.shiftKey) {
                                    e.preventDefault();
                                    handleSend();
                                }
                            }}
                            placeholder="Type your message..."
                            className="flex-1 bg-transparent border-none focus:ring-0 text-white placeholder-slate-500 max-h-32 py-3 resize-none scrollbar-hide text-sm md:text-base"
                            rows={1}
                        />

                        <div className="flex items-center gap-1">
                            <button
                                onClick={() => setVoiceLang(prev => prev === 'ar-EG' ? 'en-US' : 'ar-EG')}
                                className="text-[10px] font-bold px-2 py-1 rounded border border-white/10 text-slate-400 hover:bg-white/5 transition-colors"
                            >
                                {voiceLang === 'ar-EG' ? 'AR' : 'EN'}
                            </button>

                            {input.trim() ? (
                                <button
                                    onClick={handleSend}
                                    className="p-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl transition-all shadow-lg active:scale-95"
                                >
                                    <Send size={20} />
                                </button>
                            ) : (
                                <button
                                    onClick={handleVoiceInput}
                                    className={`p-3 rounded-xl transition-all ${isListening ? 'bg-red-500 text-white animate-pulse' : 'text-slate-400 hover:text-white hover:bg-white/5'}`}
                                >
                                    <Mic size={20} />
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatInterface;
