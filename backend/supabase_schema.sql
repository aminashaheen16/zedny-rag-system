-- Supabase Database Schema for Zedny.ai Support System

-- 1. Users Table (Lead Generation & Memory)
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  metadata JSONB DEFAULT '{}'::jsonb, -- Stores role, department, avatar, etc.
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Chat Sessions Table (Context Persistence)
CREATE TABLE IF NOT EXISTS chat_sessions (
  id TEXT PRIMARY KEY, -- Session ID (UUID string)
  user_email TEXT,
  category TEXT,
  step INTEGER DEFAULT 0,
  turn_count INTEGER DEFAULT 0,
  diagnostic_turns INTEGER DEFAULT 0,
  summary TEXT,
  status TEXT,
  history JSONB DEFAULT '[]'::jsonb,
  entities JSONB DEFAULT '{}'::jsonb,
  metadata JSONB DEFAULT '{}'::jsonb, -- Stores device_info, solutions_tried, etc.
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Migration to add metadata if table exists
-- ALTER TABLE chat_sessions ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb;

-- 3. Reports Table (Escalation Tracking)
CREATE TABLE IF NOT EXISTS reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id TEXT,
  user_email TEXT,
  category TEXT,
  service TEXT,
  urgency TEXT,
  summary TEXT,
  history JSONB DEFAULT '[]'::jsonb,
  assigned_to TEXT,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  metadata JSONB DEFAULT '{}'::jsonb
);

-- 4. Ratings Table (Feedback Loop)
CREATE TABLE IF NOT EXISTS ratings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  rating INTEGER CHECK (rating >= 1 AND rating <= 5),
  message TEXT,
  history JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS (Optional - If you want security on the client side)
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE ratings ENABLE ROW LEVEL SECURITY;
