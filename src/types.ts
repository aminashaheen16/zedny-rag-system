export interface ChatMessage {
    id: string;
    role: 'user' | 'assistant' | 'system' | 'ai'; // 'ai' mapped to 'assistant' usually
    content: string;
    timestamp: Date | string;
    category?: 'Tech' | 'Media' | 'Content' | 'Commercial' | string;
    type?: 'text' | 'escalation_prompt' | 'escalation_form' | 'success' | 'rating';
    isError?: boolean;
}

export interface Chat {
    id: string;
    title: string;
    lastMessage: string;
    lastMessageAt: Date | string;
    unreadCount?: number;
}

export interface EscalationData {
    name: string;
    email: string;
    phone: string;
    userType: 'student' | 'company' | null;
    institution?: string;
    grade?: string;
    fieldOfStudy?: string;
    companyName?: string;
    jobTitle?: string;
    description: string;
}

export interface UserProfile {
    name: string;
    email: string;
    avatar?: string;
    plan?: string;
}
