"use client";

import React, { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useAuth } from "@/context/auth-context";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { userToken, user, isLoading, isSignout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    // If auth is fully loaded and no token/user exists, redirect to login
    if (!isLoading && !userToken && !isSignout) {
      // Store the requested path so they can be redirected back after login
      const returnUrl = encodeURIComponent(pathname || "/dashboard");
      router.replace(`/login?redirect=${returnUrl}`);
    }
  }, [isLoading, userToken, isSignout, router, pathname]);

  // While checking auth status, show a loading state
  if (isLoading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-background">
        <div className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin"></div>
        <p className="mt-4 text-sm font-bold text-muted-foreground animate-pulse">Checking session...</p>
      </div>
    );
  }

  // If no token exists, don't render children (they will be redirected soon)
  if (!userToken || !user) {
    return null;
  }

  // At this point, user is authenticated
  const role = user.role;

  // Enforce role-based access to specific specialized routes if any are added in the future
  if (role === "CITIZEN" && pathname?.startsWith("/admin")) {
    router.replace("/dashboard");
    return null;
  }
  if (role === "INSPECTOR" && pathname?.startsWith("/admin")) {
    router.replace("/dashboard");
    return null;
  }

  return <>{children}</>;
}
