import Link from "next/link";
import { Button } from "@/components/ui/button";
import { createClient } from "@/lib/supabase/server";

export default async function HomePage() {
  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  return (
    <main className="container mx-auto flex min-h-screen flex-col items-center justify-center gap-6 px-4 py-16">
      <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">LoadLab</h1>
      <p className="max-w-2xl text-center text-lg text-muted-foreground">
        Precision rifle load development with statistical rigor. Node detection that tells the
        truth.
      </p>
      <div className="flex gap-3">
        {user ? (
          <Button asChild size="lg">
            <Link href="/dashboard">Go to dashboard</Link>
          </Button>
        ) : (
          <Button asChild size="lg">
            <Link href="/sign-in">Sign in</Link>
          </Button>
        )}
      </div>
    </main>
  );
}
