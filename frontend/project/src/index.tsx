import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { LeaderboardFrame } from "./screens/LeaderboardFrame";

createRoot(document.getElementById("app") as HTMLElement).render(
  <StrictMode>
    <LeaderboardFrame />
  </StrictMode>,
);
