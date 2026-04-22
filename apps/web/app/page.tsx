export default function HomePage() {
  return (
    <main className="container mx-auto flex min-h-screen flex-col items-center justify-center gap-6 px-4 py-16">
      <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">LoadLab</h1>
      <p className="max-w-2xl text-center text-lg text-muted-foreground">
        Precision rifle load development with statistical rigor. Node detection
        that tells the truth.
      </p>
      <p className="text-sm text-muted-foreground">
        Bootstrap complete. See <code className="font-mono">README.md</code> for
        next steps.
      </p>
    </main>
  );
}
