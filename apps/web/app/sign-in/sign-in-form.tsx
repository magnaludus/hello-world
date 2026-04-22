"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { createClient } from "@/lib/supabase/client";

export function SignInForm({ redirectTo }: { redirectTo: string | undefined }) {
  const supabase = createClient();
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState<"google" | "email" | null>(null);

  async function signInWithGoogle() {
    setBusy("google");
    const next = redirectTo ?? "/dashboard";
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}`,
      },
    });
    if (error) {
      toast.error(error.message);
      setBusy(null);
    }
  }

  async function signInWithEmail(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setBusy("email");
    const next = redirectTo ?? "/dashboard";
    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}`,
      },
    });
    setBusy(null);
    if (error) {
      toast.error(error.message);
      return;
    }
    toast.success("Magic link sent. Check your inbox.");
  }

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Sign in to LoadLab</CardTitle>
        <CardDescription>Precision rifle load development with statistical rigor.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Button
          type="button"
          variant="outline"
          className="w-full"
          disabled={busy !== null}
          onClick={() => void signInWithGoogle()}
        >
          {busy === "google" ? "Redirecting..." : "Continue with Google"}
        </Button>
        <div className="relative text-center text-xs text-muted-foreground">
          <span className="bg-card px-2 relative z-10">or email magic link</span>
          <div className="absolute inset-0 top-1/2 h-px bg-border" />
        </div>
        <form onSubmit={(e) => void signInWithEmail(e)} className="space-y-3">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              disabled={busy !== null}
            />
          </div>
          <Button type="submit" className="w-full" disabled={busy !== null || !email}>
            {busy === "email" ? "Sending..." : "Send magic link"}
          </Button>
        </form>
      </CardContent>
      <CardFooter className="text-xs text-muted-foreground">
        By signing in you agree to the project disclaimer. LoadLab is an analysis tool, not a reloading manual.
      </CardFooter>
    </Card>
  );
}
