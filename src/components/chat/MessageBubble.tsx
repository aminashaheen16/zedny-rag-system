import React from 'react';
import { motion } from 'framer-motion';
import { Bot, User, CheckCircle, X, Sparkles, Copy, ThumbsUp, AlertTriangle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { ChatMessage, EscalationData } from '../../types';
import { EscalationForm } from './EscalationForm';
import { StarRating } from './StarRating';

interface Props {
    message: ChatMessage;
    onEscalationResponse?: (response: 'yes' | 'no') => void;
    onFormSubmit?: (data: EscalationData) => void;
    onRate?: (rating: number) => void;
    lang?: 'en' | 'ar';
}

const MESSAGE_TRANSLATIONS = {
    en: {
        expertPrompt: 'Connect Expert',
        noThanks: 'No, thanks',
        success: 'Success'
    },
    ar: {
        expertPrompt: 'تواصل مع خبير',
        noThanks: 'لا شكراً',
        success: 'تم بنجاح'
    }
};

export const MessageBubble: React.FC<Props> = ({ message, onEscalationResponse, onFormSubmit, onRate, lang = 'en' }) => {
    const isAi = message.role === 'assistant' || message.role === 'ai';
    const isUser = message.role === 'user';
    const isSystem = message.role === 'system';

    // Auto-detect if content is primarily Arabic
    const isArabicText = /[\u0600-\u06FF]/.test(message.content);
    const isAr = lang === 'ar' || isArabicText;
    const t = MESSAGE_TRANSLATIONS[isAr ? 'ar' : 'en'];

    return (
        <motion.div
            initial={{ opacity: 0, y: 10, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className={`flex items-start gap-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
        >
            {/* Avatar */}
            <div className={`
        w-10 h-10 rounded-xl flex items-center justify-center shrink-0 shadow-lg relative
        ${isAi
                    ? 'bg-gradient-to-br from-indigo-500 to-purple-600 text-white ring-2 ring-indigo-500/20 shadow-glow'
                    : isUser
                        ? 'bg-slate-700 text-slate-200 ring-2 ring-slate-600/30'
                        : 'bg-red-900/50 text-red-200 ring-2 ring-red-500/30'}
      `}>
                {isAi && <Bot size={20} />}
                {isUser && <User size={20} />}
                {isSystem && <AlertTriangle size={20} />}

                {/* Verification Badge for AI */}
                {isAi && (
                    <div className={`absolute -bottom-1 ${isUser ? '-left-1' : '-right-1'} w-4 h-4 bg-green-500 rounded-full border-2 border-slate-900 flex items-center justify-center`}>
                        <CheckCircle size={8} className="text-white" />
                    </div>
                )}
            </div>

            {/* Bubble Content */}
            <div
                dir={isAr ? 'rtl' : 'ltr'}
                className={`
                max-w-[90%] md:max-w-[80%] rounded-2xl px-5 py-4 shadow-soft backdrop-blur-xl
                ${isAr ? 'font-arabic text-right' : 'text-left'}
                ${isUser
                        ? 'bg-gradient-to-r from-indigo-600 to-indigo-500 text-white rounded-tr-none'
                        : isSystem
                            ? 'bg-red-950/40 border border-red-500/30 text-red-100 rounded-tl-none'
                            : 'bg-slate-800/40 border border-white/5 text-slate-50 rounded-tl-none hover:bg-slate-800/60 transition-colors duration-300'}
            `}>
                {/* Category Tag (If available) */}
                {message.category && isAi && (
                    <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-indigo-500/10 text-[10px] md:text-xs font-medium mb-3 border border-indigo-500/20 ${isAr ? 'flex-row-reverse' : ''}`}>
                        <Sparkles className="w-3 h-3 text-amber-400" />
                        <span className="text-indigo-200 uppercase tracking-wide">{message.category} Analysis</span>
                    </div>
                )}

                {/* Type: Text (Standard) */}
                {(!message.type || message.type === 'text') && (
                    <div className={`prose prose-invert prose-sm md:prose-base max-w-none leading-relaxed break-words overflow-hidden ${isAr ? 'text-right' : 'text-left'}`}>
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {message.content}
                        </ReactMarkdown>
                    </div>
                )}

                {/* Type: Escalation Prompt */}
                {message.type === 'escalation_prompt' && (
                    <div className="space-y-4">
                        <p className="font-medium text-white text-base">{message.content}</p>
                        <div className={`flex gap-3 pt-2 ${isAr ? 'flex-row-reverse' : ''}`}>
                            <button
                                onClick={() => onEscalationResponse?.('yes')}
                                className="flex items-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-sm font-bold transition-all shadow-lg shadow-indigo-600/30 active:scale-95"
                            >
                                <CheckCircle className="w-4 h-4" /> {t.expertPrompt}
                            </button>
                            <button
                                onClick={() => onEscalationResponse?.('no')}
                                className="flex items-center gap-2 px-5 py-2.5 bg-white/5 hover:bg-white/10 text-slate-300 rounded-xl text-sm font-medium transition-colors border border-white/5 active:scale-95"
                            >
                                <X className="w-4 h-4" /> {t.noThanks}
                            </button>
                        </div>
                    </div>
                )}

                {/* Type: Escalation Form */}
                {message.type === 'escalation_form' && onFormSubmit && (
                    <EscalationForm onSubmit={onFormSubmit} lang={isAr ? 'ar' : 'en'} />
                )}

                {/* Type: Rate */}
                {message.type === 'rating' && onRate && (
                    <StarRating onSubmit={onRate} />
                )}

                {/* Type: Success */}
                {message.type === 'success' && (
                    <div className={`flex items-start gap-4 ${isAr ? 'flex-row-reverse' : ''}`}>
                        <div className="p-2 bg-green-500/10 rounded-full border border-green-500/20">
                            <CheckCircle className="w-6 h-6 text-green-400" />
                        </div>
                        <div className={isAr ? 'text-right' : 'text-left'}>
                            <h4 className="text-white font-bold text-lg mb-1">{t.success}</h4>
                            <p className="text-slate-400 text-sm">{message.content}</p>
                        </div>
                    </div>
                )}

                {/* Footer Info */}
                <div className="flex items-center justify-between mt-3 pt-2 border-t border-white/5">
                    <span className="text-[10px] opacity-40 font-medium">
                        {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>

                    {isAi && (
                        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button className="text-slate-500 hover:text-indigo-400 transition-colors" title="Copy">
                                <Copy size={12} />
                            </button>
                            <button className="text-slate-500 hover:text-green-400 transition-colors" title="Helpful">
                                <ThumbsUp size={12} />
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </motion.div>
    );
};
