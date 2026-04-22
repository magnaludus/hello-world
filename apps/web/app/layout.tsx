import type { Metadata } from "next";
import { Toaster } from "@/components/ui/toaster";
import { TRPCProvider } from "@/lib/trpc/client";
import "./globals.css";

export const metadata: Metadata = {
  title: "LoadLab",
  description: "Precision rifle load development with statistical rigor.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-background font-sans antialiased">
        <TRPCProvider>
          {children}
          <Toaster />
        </TRPCProvider>
      </body>
    </html>
  );
}
