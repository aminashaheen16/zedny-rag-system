
import { Routes, Route, Navigate } from 'react-router-dom';
import ChatInterface from './components/chat/ChatInterface';
import LandingPage from './pages/LandingPage';

function App() {
    return (
        <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/chat" element={<ChatInterface />} />
            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
    );
}

export default App;
