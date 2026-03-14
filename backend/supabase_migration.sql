-- Run this in your Supabase SQL Editor to support the new rich reports

-- 1. Add Phone and Company columns
ALTER TABLE reports 
ADD COLUMN IF NOT EXISTS user_phone TEXT,
ADD COLUMN IF NOT EXISTS company_name TEXT;

-- 2. Ensure ID is UUID if not already
-- (Note: If your ID is already UUID, this is just for safety)
-- ALTER TABLE reports ALTER COLUMN id SET DATA TYPE UUID USING id::uuid;
