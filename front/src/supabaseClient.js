import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://czvodiqotcyurmkwgahs.supabase.co";
const supabaseAnonKey =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN6dm9kaXFvdGN5dXJta3dnYWhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY1NTY1MzksImV4cCI6MjA4MjEzMjUzOX0.iWg9O2W813Ks5ncPZ0ecea5LpJP3RIJe6PgEs_Fp6nQ";

console.log("URL:", supabaseUrl);
export const supabase = createClient(supabaseUrl, supabaseAnonKey);
