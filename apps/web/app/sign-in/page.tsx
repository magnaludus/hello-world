import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { SignInForm } from "./sign-in-form";

export default async function SignInPage({
  searchParams,
}: {
  searchParams: { redirect?: string };
}) {
  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (user) redirect(searchParams.redirect ?? "/dashboard");

  return (
    <main className="container mx-auto flex min-h-screen items-center justify-center px-4">
      <SignInForm redirectTo={searchParams.redirect} />
    </main>
  );
}
