import type { User } from "@supabase/supabase-js";
import { createClient } from "@/lib/supabase/server";

export type Context = {
  user: User | null;
  supabase: ReturnType<typeof createClient>;
};

export async function createContext(): Promise<Context> {
  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  return { supabase, user };
}
