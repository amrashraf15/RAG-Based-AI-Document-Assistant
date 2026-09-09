import { useEffect, useState } from "react";

import { getHealth } from "../api/health";
import type { HealthResponse } from "../types/api";

export function useHealth() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    const checkHealth = async () => {
      try {
        const response = await getHealth();

        console.log("HEALTH RESPONSE:", response);
        console.log("STATUS:", response.status);
        console.log(
          "RAG INITIALIZED:",
          response.rag_initialized,
        );

        if (mounted) {
          setHealth(response);
        }
      } catch (error) {
        console.error("HEALTH CHECK FAILED:", error);

        if (mounted) {
          setHealth(null);
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    void checkHealth();

    const interval = window.setInterval(
      checkHealth,
      30000,
    );

    return () => {
      mounted = false;
      window.clearInterval(interval);
    };
  }, []);

  const connected =
    health?.status === "ok" &&
    health?.rag_initialized === true;

  console.log("HEALTH STATE:", health);
  console.log("CONNECTED:", connected);

  return {
    health,
    loading,
    connected,
  };
}