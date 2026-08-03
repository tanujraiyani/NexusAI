"use client";

import { useEffect, useState } from "react";
import { api } from "../lib/api";

export default function Home() {
  const [message, setMessage] = useState("Loading...");

  useEffect(() => {
    async function loadHealth() {
      try {
        const response = await api.get("/health");
        setMessage(response.data.status);
      } catch (error) {
        console.error(error);
        setMessage("Backend connection failed");
      }
    }

    loadHealth();
  }, []);

  return (
    <main
      style={{
        padding: "40px",
        fontFamily: "sans-serif",
      }}
    >
      <h1>NexusAI</h1>

      <h2>Gateway Status</h2>

      <p>{message}</p>
    </main>
  );
}