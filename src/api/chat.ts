export interface ChatRequest {
    message: string;
    department?: string;
    user_email?: string;
    session_id?: string;
    // Use 'Record<string, any>' for flexible technical profile data
    technical_profile?: Record<string, any>;
    // Allow passing back the incident state for stateless backends
    incident_state?: any;
}

export interface ChatResponse {
    answer: string;
    should_escalate: boolean;
    context_used?: string;
    incident_state?: any;
    action_required?: string;
}

// Ensure this matches your running backend port
const API_BASE_URL = 'http://localhost:8000';

export const chatApi = {
    async sendMessage(payload: ChatRequest): Promise<ChatResponse> {
        try {
            const response = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                // Try to parse error details if available
                let errorMsg = response.statusText;
                try {
                    const errData = await response.json();
                    if (errData.detail) errorMsg = errData.detail;
                } catch (_) { /* ignore parse error */ }

                throw new Error(`API Error: ${response.status} - ${errorMsg}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Chat API Error:', error);
            throw error;
        }
    },

    async submitRating(payload: { session_id: string; rating: number; message?: string; history?: string[]; user_email?: string }) {
        try {
            const response = await fetch(`${API_BASE_URL}/rate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error(`Rating API Error: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Rating API Error:', error);
            throw error;
        }
    },

    async submitReport(payload: any) {
        try {
            console.log("🚀 Submitting Report Payload:", payload); // Debug log
            const response = await fetch(`${API_BASE_URL}/reports`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                let errorDetails = response.statusText;
                try {
                    const text = await response.text();
                    errorDetails = text;
                } catch (e) { /* ignore */ }
                throw new Error(`Report API Error: ${response.status} - ${errorDetails}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Report API Error:', error);
            throw error;
        }
    }
};
