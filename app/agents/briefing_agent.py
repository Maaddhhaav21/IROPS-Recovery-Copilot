import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class BriefingAgent:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not set."
            )

        self.llm = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0.2,
            api_key=api_key,
        )

    def generate(self, state):

        flight_id = state["flight_id"]

        affected_passengers = state.get(
            "affected_passengers", []
        )

        connecting_passengers = state.get(
            "connecting_passengers", []
        )

        rebooking_results = state.get(
            "rebooking_results", []
        )

        crew_analysis = state.get(
            "crew_analysis", {}
        )

        # -----------------------------
        # Deterministic facts
        # -----------------------------

        affected_count = len(
            affected_passengers
        )

        connecting_count = len(
            connecting_passengers
        )

        rebooked_count = sum(
            result.get("status") == "REBOOKED"
            for result in rebooking_results
        )

        unresolved_count = sum(
            result.get("status") != "REBOOKED"
            for result in rebooking_results
        )

        available_crew = len(
            crew_analysis.get(
                "available_crew", []
            )
        )

        matching_crew = len(
            crew_analysis.get(
                "matching_crew", []
            )
        )

        aircraft_type = crew_analysis.get(
            "aircraft_type",
            "UNKNOWN"
        )

        disruption_type = state.get(
            "disruption_type",
            "UNKNOWN"
        )

        severity = state.get(
            "severity",
            "UNKNOWN"
        )

        solver_status = state.get(
            "solver_status",
            "UNKNOWN"
        )

        disruption_status = state.get(
            "disruption_status",
            "UNKNOWN"
        )

        # -----------------------------
        # Facts passed to the LLM
        # -----------------------------

        recovery_data = {
            "flight_id": flight_id,
            "disruption_type": disruption_type,
            "severity": severity,
            "disruption_status": disruption_status,
            "affected_passengers": affected_count,
            "connecting_passengers": connecting_count,
            "rebooked_passengers": rebooked_count,
            "unresolved_passengers": unresolved_count,
            "solver_status": solver_status,
            "aircraft_type": aircraft_type,
            "available_crew": available_crew,
            "matching_crew": matching_crew,
        }

        # -----------------------------
        # Strict LLM instructions
        # -----------------------------

        system_prompt = """
You are an Airline Operations Recovery Copilot.

Analyze the recovery data provided by the deterministic
airline recovery system.

Your task is to produce a concise operational briefing.

IMPORTANT:

1. Treat the supplied recovery data as the ONLY source of facts.

2. NEVER invent:
   - flights
   - passenger details
   - crew details
   - aircraft status
   - departure times
   - arrival times
   - airport information
   - maintenance information
   - fueling information
   - operational events

3. Do not claim that connecting passengers were successfully
   accommodated unless that information is explicitly provided.

4. Do not claim that an aircraft is ready, unavailable,
   maintained, fueled, or operational unless explicitly provided.

5. OR-Tools is the source of truth for rebooking results.

6. Clearly distinguish:
   - what the system KNOWS
   - what remains unresolved
   - what operations SHOULD investigate or do next

7. Recommendations are allowed, but clearly label them
   as recommendations rather than facts.

8. Be concise and professional.

Use this structure:

CURRENT SITUATION
SUCCESSFULLY RECOVERED
REMAINING ISSUES
RECOMMENDED ACTION
OVERALL ASSESSMENT
"""

        user_prompt = f"""
Here is the deterministic recovery data:

{json.dumps(recovery_data, indent=2)}

Generate the operational briefing.
"""

        # -----------------------------
        # LLM call
        # -----------------------------

        response = self.llm.invoke(
            [
                ("system", system_prompt),
                ("human", user_prompt),
            ]
        )

        briefing = response.content

        return {
            "status": "BRIEFING_GENERATED",
            "flight_id": flight_id,
            "briefing": briefing,
            "recovery_data": recovery_data,
        }