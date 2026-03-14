import React from 'react';
import { motion } from 'framer-motion';
import { MessageSquare, Plus, Clock, Bot } from 'lucide-react';
import type { Chat } from '../../types';

interface ChatSidebarProps {
    chats: Chat[];
    activeChatId: string | null;
    onSelectChat: (chat: Chat) => void;
    onNewChat: () => void;
    isOpen: boolean;
}

export const ChatSidebar: React.FC<ChatSidebarProps> = ({
    chats,
    activeChatId,
    onSelectChat,
    onNewChat,
    isOpen
}) => {
    return (
        <div className={`
            fixed inset-y-0 left-0 w-80 bg-slate-900/95 backdrop-blur-xl border-r border-indigo-500/10 
            flex flex-col z-40 transform transition-transform duration-300 
            md:relative md:translate-x-0 
            ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}>
            {/* Header */}
            <div className="h-20 flex items-center px-6 border-b border-indigo-500/10 bg-slate-900/50">
                <div className="flex items-center gap-3">
                    <div className="relative">
                        <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg blur opacity-50" />
                        <div className="relative w-9 h-9 rounded-lg bg-slate-900 flex items-center justify-center border border-indigo-500/30">
                            <Bot className="w-5 h-5 text-indigo-400" />
                        </div>
                    </div>
                    <div>
                        <span className="font-bold text-lg tracking-tight text-white block">ZEDNY.AI</span>
                        <span className="text-[10px] text-indigo-400 font-medium tracking-widest uppercase">Enterprise</span>
                    </div>
                </div>
            </div>

            {/* New Chat Button */}
            <div className="p-5">
                <button
                    onClick={onNewChat}
                    className="w-full h-11 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg shadow-indigo-500/20 text-sm font-semibold active:scale-[0.98]"
                >
                    <Plus className="w-4 h-4" />
                    New Conversation
                </button>
            </div>

            {/* Chat List */}
            <div className="flex-1 overflow-y-auto px-3 space-y-1 scrollbar-thin scrollbar-thumb-indigo-500/10">
                <div className="px-4 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                    Recent History
                </div>

                {chats.length === 0 && (
                    <div className="text-center py-10 px-6">
                        <Clock className="w-8 h-8 text-slate-700 mx-auto mb-3" />
                        <p className="text-sm text-slate-500">No recent chats.</p>
                        <p className="text-xs text-slate-600">Start a new conversation to get help.</p>
                    </div>
                )}

                {chats.map((chat) => (
                    <motion.button
                        key={chat.id}
                        onClick={() => onSelectChat(chat)}
                        whileHover={{ x: 4 }}
                        className={`
                            w-full text-left p-3 rounded-xl flex items-start gap-3 transition-all group relative
                            ${activeChatId === chat.id
                                ? 'bg-indigo-500/10 border border-indigo-500/20 shadow-lg shadow-indigo-500/5'
                                : 'hover:bg-white/5 border border-transparent'
                            }
                        `}
                    >
                        <MessageSquare className={`w-5 h-5 mt-0.5 flex-shrink-0 ${activeChatId === chat.id ? 'text-indigo-400' : 'text-slate-500 group-hover:text-indigo-300'}`} />

                        <div className="flex-1 min-w-0">
                            <h3 className={`text-sm font-medium truncate ${activeChatId === chat.id ? 'text-white' : 'text-slate-400 group-hover:text-slate-200'}`}>
                                {chat.title}
                            </h3>
                            <p className="text-[10px] text-slate-600 mt-1 flex items-center gap-1 group-hover:text-slate-500">
                                <Clock className="w-3 h-3" />
                                {new Date(chat.lastMessageAt).toLocaleDateString()}
                            </p>
                        </div>
                    </motion.button>
                ))}
            </div>

            {/* User Profile */}
            <div className="p-4 border-t border-indigo-500/10 bg-slate-900/50">
                <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-full bg-gradient-to-br from-slate-700 to-slate-900 border border-white/10 flex items-center justify-center shadow-lg">
                        <span className="text-xs font-bold text-slate-300">GU</span>
                    </div>
                    <div className="flex-1">
                        <p className="text-sm font-semibold text-white">Guest User</p>
                        <div className="flex items-center gap-1.5">
                            <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                            <p className="text-[10px] text-slate-400">System Online</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
