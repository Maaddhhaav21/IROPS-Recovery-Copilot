/* =================================================================
   IROPS RECOVERY COPILOT — FRONTEND CONTROLLER
   Talks to the existing FastAPI backend at API_BASE_URL.
   This file only renders whatever the backend returns — it never
   invents, hard-codes, or simulates recovery data.
   ================================================================= */

const API_BASE_URL = "http://127.0.0.1:8000";
const REQUEST_TIMEOUT_MS = 90000; // LangGraph + OR-Tools + LLM can take a while

// How long each loading-step bullet stays highlighted before the next
// one lights up. This is purely a visual heartbeat — it does NOT
// reflect real backend progress, since the API gives us none.
const LOADING_STEP_INTERVAL_MS = 2200;

// ---- DOM references -------------------------------------------------
const flightIdInput = document.getElementById("flightIdInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const analyzeBtnLabel = document.getElementById("analyzeBtnLabel");
const resetBtn = document.getElementById("resetBtn");

const emptyState = document.getElementById("emptyState");
const loadingState = document.getElementById("loadingState");
const resultsWrap = document.getElementById("resultsWrap");
const errorBanner = document.getElementById("errorBanner");
const errorTitle = document.getElementById("errorTitle");
const errorMessage = document.getElementById("errorMessage");

const lastAnalyzedWrap = document.getElementById("lastAnalyzedWrap");
const lastAnalyzedFlight = document.getElementById("lastAnalyzedFlight");
const lastAnalyzedTime = document.getElementById("lastAnalyzedTime");

const systemStatusDot = document.getElementById("systemStatusDot");
const systemStatusText = document.getElementById("systemStatusText");

let loadingStepTimer = null;

// ======================================================================
// EVENT WIRING
// ======================================================================

analyzeBtn.addEventListener("click", analyzeRecovery);
resetBtn.addEventListener("click", resetDashboard);

// Allow pressing Enter inside the flight ID field to trigger analysis.
flightIdInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    analyzeRecovery();
  }
});

// ======================================================================
// CORE FLOW
// ======================================================================

/**
 * Reads the flight ID, calls the backend /recover endpoint, and
 * renders the response. This is the main entry point for the
 * "Analyze Recovery" button.
 */
async function analyzeRecovery() {
  const flightId = flightIdInput.value.trim();

  if (!flightId) {
    showError(
      "Flight ID required",
      "Enter a flight ID (for example, FL0001) before running the recovery engine.",
    );
    return;
  }

  hideError();
  showLoading();
  setAnalyzeButtonBusy(true);

  const controller = new AbortController();
  const timeoutHandle = setTimeout(
    () => controller.abort(),
    REQUEST_TIMEOUT_MS,
  );

  try {
    const response = await fetch(`${API_BASE_URL}/recover`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ flight_id: flightId }),
      signal: controller.signal,
    });

    if (!response.ok) {
      handleHttpError(response.status);
      return;
    }

    let data;
    try {
      data = await response.json();
    } catch (parseErr) {
      showError(
        "Malformed response",
        "The recovery engine returned a response that could not be read. Please try again.",
      );
      return;
    }

    displayRecoveryData(data);
    markSystemOperational();
    recordLastAnalyzed(data.flight_id || flightId);
  } catch (err) {
    if (err.name === "AbortError") {
      showError(
        "Request timed out",
        "The recovery engine is taking longer than expected. It may still be processing — please try again shortly.",
      );
    } else {
      // Most commonly: FastAPI server isn't running, or a network/CORS issue.
      showError(
        "Unable to connect to the recovery engine",
        "Please ensure the FastAPI backend is running at " + API_BASE_URL + ".",
      );
      markSystemDown();
    }
  } finally {
    clearTimeout(timeoutHandle);
    setAnalyzeButtonBusy(false);
    hideLoading();
  }
}

/**
 * Maps HTTP status codes to a readable error message without ever
 * surfacing a raw stack trace or JS exception to the user.
 */
function handleHttpError(status) {
  if (status === 404) {
    showError(
      "Flight not found",
      "No record matches that flight ID. Double-check the ID and try again.",
    );
  } else if (status === 422) {
    showError(
      "Invalid flight ID",
      "The recovery engine could not process that flight ID. Check the format and try again.",
    );
  } else if (status >= 500) {
    showError(
      "Recovery engine error",
      "The backend encountered an error while processing this flight. Please try again.",
    );
  } else {
    showError(
      "Request failed",
      `The recovery engine returned an unexpected error (HTTP ${status}).`,
    );
  }
}

/**
 * Fans the API response out to each section-specific render function.
 */
function displayRecoveryData(data) {
  displayDisruption(data);
  displayPassengerImpact(data);
  displayOptimization(data);
  displayCrew(data.crew || {});
  displayPassengerRecovery(data.passenger_recovery || []);
  displayAlternativeFlights(data.alternative_flights || []);
  displayBriefing(data.briefing);

  resultsWrap.classList.remove("hidden");
  emptyState.classList.add("hidden");
}

// ======================================================================
// SECTION RENDERERS
// ======================================================================

function displayDisruption(data) {
  document.getElementById("disFlightId").textContent = data.flight_id || "—";
  document.getElementById("disType").textContent = formatLabel(
    data.disruption_type,
  );

  const severityEl = document.getElementById("disSeverity");
  const severity = (data.severity || "").toUpperCase();
  severityEl.textContent = severity || "—";
  severityEl.className = "badge " + severityClass(severity);

  const statusEl = document.getElementById("disStatus");
  const status = deriveOperationalStatus(data);
  statusEl.textContent = status;
  statusEl.className = "badge " + severityClass(severity, true);
}

/**
 * The API does not send an explicit "status" field like CANCELLED —
 * we derive a readable operational label from what it does send,
 * without inventing new facts about the flight.
 */
function deriveOperationalStatus(data) {
  if (typeof data.unresolved === "number" && data.unresolved > 0) {
    return "PARTIALLY RECOVERED";
  }
  if (data.solver_status && data.solver_status.toUpperCase() === "OPTIMAL") {
    return "RECOVERED";
  }
  return "UNDER REVIEW";
}

function severityClass(severity, neutral) {
  if (severity === "LOW") return "badge--low";
  if (severity === "MEDIUM") return "badge--medium";
  if (severity === "HIGH") return "badge--high";
  return neutral ? "badge--neutral" : "";
}

function displayPassengerImpact(data) {
  document.getElementById("statAffected").textContent = formatNumber(
    data.affected_passengers,
  );
  document.getElementById("statConnecting").textContent = formatNumber(
    data.connecting_passengers,
  );
  document.getElementById("statRebooked").textContent = formatNumber(
    data.rebooked,
  );
  document.getElementById("statUnresolved").textContent = formatNumber(
    data.unresolved,
  );

  const unresolvedCard = document.getElementById("unresolvedCard");
  if (typeof data.unresolved === "number" && data.unresolved > 0) {
    unresolvedCard.classList.add("has-unresolved");
  } else {
    unresolvedCard.classList.remove("has-unresolved");
  }
}

function displayOptimization(data) {
  const solverStatusEl = document.getElementById("solverStatus");
  const solverStatus = (data.solver_status || "UNKNOWN").toUpperCase();
  solverStatusEl.textContent = solverStatus;
  solverStatusEl.className =
    "badge " +
    (solverStatus === "OPTIMAL"
      ? "badge--solver-optimal"
      : "badge--solver-warning");

  const rebooked = Number(data.rebooked) || 0;
  const affected = Number(data.affected_passengers) || 0;

  document.getElementById("recoverySummary").textContent =
    `${formatNumber(data.rebooked)} / ${formatNumber(data.affected_passengers)} passengers successfully rebooked`;

  const percent =
    affected > 0 ? Math.min(100, Math.round((rebooked / affected) * 100)) : 0;
  const fillEl = document.getElementById("recoveryProgressFill");
  // Reset then apply on next frame so the width transition animates in.
  fillEl.style.width = "0%";
  requestAnimationFrame(() => {
    fillEl.style.width = percent + "%";
  });

  document.getElementById("recoveryProgressCaption").textContent =
    affected > 0
      ? `${percent}% of affected passengers rebooked`
      : "No affected passengers reported";
}

function displayCrew(crew) {
  document.getElementById("crewAircraftType").textContent =
    crew.aircraft_type || "—";
  document.getElementById("crewAvailable").textContent = formatNumber(
    crew.available_crew,
  );
  document.getElementById("crewMatching").textContent = formatNumber(
    crew.matching_crew,
  );

  const crewAlert = document.getElementById("crewAlert");
  const available = Number(crew.available_crew);
  const matching = Number(crew.matching_crew);

  // "Significantly lower" heuristic: matching crew is less than half of
  // available crew, and there is at least one available crew member.
  const needsAttention =
    Number.isFinite(available) &&
    Number.isFinite(matching) &&
    available > 0 &&
    matching < available * 0.5;

  crewAlert.classList.toggle("hidden", !needsAttention);
}

/**
 * Renders the LLM-generated briefing. The briefing may use
 * **SECTION TITLE** markers — this splits on those markers and
 * renders each as its own block. If no markers are present, the
 * whole briefing is shown as a single block. Text is always inserted
 * via textContent, never innerHTML, to avoid rendering raw markup.
 */
function displayPassengerRecovery(passengers) {
  const body = document.getElementById("passengerRecoveryBody");
  const tag = document.getElementById("passengerRecoveryTag");

  body.innerHTML = "";

  if (!Array.isArray(passengers) || passengers.length === 0) {
    tag.textContent = "0 passengers";

    body.innerHTML = `
      <tr>
        <td colspan="5" class="table-empty">
          No passenger recovery decisions were returned.
        </td>
      </tr>
    `;

    return;
  }

  const rebooked = passengers.filter(
    (passenger) => passenger.status === "REBOOKED",
  ).length;

  const unresolved = passengers.length - rebooked;

  tag.textContent = `${rebooked} rebooked · ${unresolved} unresolved`;

  passengers.forEach((passenger) => {
    const row = document.createElement("tr");

    const status = String(passenger.status || "UNKNOWN").toUpperCase();

    const isRebooked = status === "REBOOKED";

    row.innerHTML = `
      <td class="flight-cell">
        ${escapeHtml(passenger.passenger_id || "—")}
      </td>

      <td>
        ${escapeHtml(passenger.original_flight || "—")}
      </td>

      <td class="${passenger.new_flight ? "flight-cell" : "table-muted"}">
        ${escapeHtml(passenger.new_flight || "—")}
      </td>

      <td>
        <span class="table-status ${
          isRebooked ? "table-status--success" : "table-status--warning"
        }">
          ${escapeHtml(status)}
        </span>
      </td>

      <td class="reason-cell">
        ${escapeHtml(passenger.reason || "—")}
      </td>
    `;

    body.appendChild(row);
  });
}

function displayAlternativeFlights(flights) {
  const body = document.getElementById("alternativeFlightsBody");

  const tag = document.getElementById("alternativeFlightsTag");

  body.innerHTML = "";

  if (!Array.isArray(flights) || flights.length === 0) {
    tag.textContent = "0 alternatives";

    body.innerHTML = `
      <tr>
        <td colspan="6" class="table-empty">
          No alternative flights were found.
        </td>
      </tr>
    `;

    return;
  }

  tag.textContent = `${flights.length} alternatives`;

  flights.forEach((flight) => {
    const row = document.createElement("tr");

    const availableSeats = Number(flight.available_seats);

    const seatText = Number.isFinite(availableSeats)
      ? availableSeats.toLocaleString()
      : "—";

    row.innerHTML = `
      <td class="flight-cell">
        ${escapeHtml(flight.flight_id || "—")}
      </td>

      <td class="route-cell">
        ${escapeHtml(flight.origin || "—")}
        →
        ${escapeHtml(flight.destination || "—")}
      </td>

      <td>
        ${escapeHtml(formatDateTime(flight.departure))}
      </td>

      <td>
        ${escapeHtml(formatDateTime(flight.arrival))}
      </td>

      <td>
        ${seatText}
      </td>

      <td>
        <span class="table-status table-status--neutral">
          ${escapeHtml(flight.status || "—")}
        </span>
      </td>
    `;

    body.appendChild(row);
  });
}

function formatDateTime(value) {
  if (!value) {
    return "—";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return String(value);
  }

  return date.toLocaleString();
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function displayBriefing(briefingText) {
  const container = document.getElementById("briefingBody");

  container.innerHTML = "";

  if (
    !briefingText ||
    typeof briefingText !== "string" ||
    !briefingText.trim()
  ) {
    const empty = document.createElement("p");

    empty.className = "briefing-section-text";

    empty.textContent = "No operational briefing was returned for this flight.";

    container.appendChild(empty);

    return;
  }

  /*
   * Only treat bold text on its own line as a section heading.
   *
   * This prevents things such as:
   *
   * **FL0001**
   * **OPTIMAL**
   *
   * from accidentally becoming section headings.
   */

  const lines = briefingText.replace(/\r\n/g, "\n").split("\n");

  const sections = [];

  let currentTitle = null;
  let currentContent = [];

  for (const line of lines) {
    const trimmed = line.trim();

    /*
     * Match headings such as:
     *
     * **CURRENT SITUATION**
     * **SUCCESSFULLY RECOVERED**
     * **REMAINING ISSUES**
     * **RECOMMENDED ACTION**
     * **OVERALL ASSESSMENT**
     *
     * The entire line must be bold.
     */

    const headingMatch = trimmed.match(/^\*\*([^*]+)\*\*$/);

    if (headingMatch) {
      if (currentTitle !== null || currentContent.length > 0) {
        sections.push({
          title: currentTitle,
          content: currentContent.join("\n").trim(),
        });
      }

      currentTitle = headingMatch[1].trim();
      currentContent = [];
    } else {
      currentContent.push(line);
    }
  }

  /*
   * Add final section.
   */

  if (currentTitle !== null || currentContent.length > 0) {
    sections.push({
      title: currentTitle,
      content: currentContent.join("\n").trim(),
    });
  }

  /*
   * Render sections.
   */

  if (sections.length === 0) {
    container.appendChild(buildBriefingSection(null, briefingText.trim()));

    return;
  }

  sections.forEach((section) => {
    if (!section.content && !section.title) {
      return;
    }

    container.appendChild(buildBriefingSection(section.title, section.content));
  });
}

function buildBriefingSection(title, content) {
  const section = document.createElement("div");

  section.className = "briefing-section";

  if (title) {
    const titleEl = document.createElement("p");

    titleEl.className = "briefing-section-title";

    titleEl.textContent = title;

    section.appendChild(titleEl);
  }

  if (content) {
    /*
     * Preserve bullet points and paragraphs.
     */

    const lines = content
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0);

    lines.forEach((line) => {
      const textEl = document.createElement("p");

      textEl.className = "briefing-section-text";

      /*
       * Remove Markdown formatting that is not
       * useful in the plain HTML presentation.
       */

      line = line
        .replace(/^\-\s*/, "• ")
        .replace(/^\*\s*/, "• ")
        .replace(/\*\*(.*?)\*\*/g, "$1");

      textEl.textContent = line;

      section.appendChild(textEl);
    });
  }

  return section;
}
// ======================================================================
// LOADING / EMPTY / ERROR STATE HELPERS
// ======================================================================

function showLoading() {
  emptyState.classList.add("hidden");
  resultsWrap.classList.add("hidden");
  loadingState.classList.remove("hidden");
  animateLoadingSteps();
}

function hideLoading() {
  loadingState.classList.add("hidden");
  stopLoadingStepAnimation();
}

/**
 * Cycles a highlight through the loading step list purely as a visual
 * heartbeat. It does not claim to know real backend progress.
 */
function animateLoadingSteps() {
  const steps = Array.from(
    document.querySelectorAll("#loadingState .loading-steps li"),
  );
  let activeIndex = 0;

  steps.forEach((step) => step.classList.remove("is-active", "is-done"));

  function highlightStep(index) {
    steps.forEach((step, i) => {
      step.classList.toggle("is-active", i === index);
      step.classList.toggle("is-done", i < index);
    });
  }

  highlightStep(0);

  loadingStepTimer = setInterval(() => {
    activeIndex = Math.min(activeIndex + 1, steps.length - 1);
    highlightStep(activeIndex);
    if (activeIndex === steps.length - 1) {
      clearInterval(loadingStepTimer);
    }
  }, LOADING_STEP_INTERVAL_MS);
}

function stopLoadingStepAnimation() {
  if (loadingStepTimer) {
    clearInterval(loadingStepTimer);
    loadingStepTimer = null;
  }
}

function showError(title, message) {
  errorTitle.textContent = title;
  errorMessage.textContent = message;
  errorBanner.classList.remove("hidden");
}

function hideError() {
  errorBanner.classList.add("hidden");
}

function setAnalyzeButtonBusy(isBusy) {
  analyzeBtn.disabled = isBusy;
  analyzeBtnLabel.textContent = isBusy ? "Analyzing…" : "Analyze Recovery";
}

/**
 * Resets the dashboard back to its initial empty state, clearing
 * any previous results and the flight ID field.
 */
function resetDashboard() {
  hideError();
  hideLoading();
  resultsWrap.classList.add("hidden");
  emptyState.classList.remove("hidden");
  flightIdInput.value = "";
  lastAnalyzedWrap.classList.add("hidden");
  flightIdInput.focus();
}

function recordLastAnalyzed(flightId) {
  lastAnalyzedFlight.textContent = flightId;
  lastAnalyzedTime.textContent = new Date().toLocaleString();
  lastAnalyzedWrap.classList.remove("hidden");
}

function markSystemOperational() {
  systemStatusDot.className = "status-dot status-dot--ok";
  systemStatusText.textContent = "System Operational";
}

function markSystemDown() {
  systemStatusDot.className = "status-dot status-dot--danger";
  systemStatusText.textContent = "Recovery Engine Unreachable";
}

// ======================================================================
// FORMATTING HELPERS
// ======================================================================

function formatNumber(value) {
  return typeof value === "number" && !Number.isNaN(value)
    ? value.toLocaleString()
    : "—";
}

function formatLabel(value) {
  if (!value || typeof value !== "string") return "—";
  return value.replace(/_/g, " ");
}

// ======================================================
// IROPS RAG POLICY ASSISTANT
// ======================================================

document.addEventListener("DOMContentLoaded", () => {

  const chatInput = document.getElementById("chatInput");
  const chatSendBtn = document.getElementById("chatSendBtn");
  const chatMessages = document.getElementById("chatMessages");

  if (!chatInput || !chatSendBtn || !chatMessages) {
    console.error("RAG chat elements not found.");
    return;
  }

  function addChatMessage(message, type) {

    const messageDiv = document.createElement("div");

    messageDiv.className =
      type === "user"
        ? "chat-message user-message"
        : "chat-message assistant-message";

    const label = document.createElement("div");
    label.className = "chat-label";
    label.textContent =
      type === "user" ? "YOU" : "IROPS ASSISTANT";

    const text = document.createElement("div");
    text.className = "chat-text";
    text.textContent = message;

    messageDiv.appendChild(label);
    messageDiv.appendChild(text);

    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;
  }


  async function askPolicyAssistant() {

    const question = chatInput.value.trim();

    if (!question) {
      return;
    }

    addChatMessage(question, "user");

    chatInput.value = "";

    chatSendBtn.disabled = true;
    chatSendBtn.textContent = "Asking...";

    try {

      const response = await fetch(
        `${API_BASE_URL}/chat?question=${encodeURIComponent(question)}`,
        {
          method: "POST"
        }
      );

      if (!response.ok) {

        const errorText = await response.text();

        throw new Error(
          `Backend error ${response.status}: ${errorText}`
        );
      }

      const data = await response.json();

      let answer = data.answer || "No answer returned.";

      if (data.sources && data.sources.length > 0) {

        answer += "\n\nSources:\n";

        data.sources.forEach(source => {

          if (source.source) {
            answer += `• ${source.source}\n`;
          }

        });
      }

      addChatMessage(answer, "assistant");

    } catch (error) {

      console.error("RAG CHAT ERROR:", error);

      addChatMessage(
        "Unable to contact the IROPS policy assistant.\n\n" +
        error.message,
        "assistant"
      );

    } finally {

      chatSendBtn.disabled = false;
      chatSendBtn.textContent = "Ask";
    }
  }


  chatSendBtn.addEventListener(
    "click",
    askPolicyAssistant
  );


  chatInput.addEventListener(
    "keydown",
    (event) => {

      if (event.key === "Enter") {
        askPolicyAssistant();
      }

    }
  );

});