import os
import re
import json
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict, Tuple

from app.models.car import Car
from app.services.web_search import web_search_tool


@dataclass
class ToolCallRecord:
    tool: str
    args: Dict[str, Any]
    result_summary: str


@dataclass
class AgentResult:
    answer: str
    tool_calls: List[ToolCallRecord] = field(default_factory=list)


# ── OpenAI tool definitions ───────────────────────────────────────────────────

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "list_current_cars",
            "description": "List all cars currently shown in the search results page.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_vehicle_details",
            "description": "Get full details of a specific car by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "car_id": {"type": "string", "description": "The ID of the car to look up"}
                },
                "required": ["car_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_cars",
            "description": "Compare two or more cars side-by-side on price, mileage, year, and value.",
            "parameters": {
                "type": "object",
                "properties": {
                    "car_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of car IDs to compare",
                    }
                },
                "required": ["car_ids"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_saved_cars",
            "description": "Retrieve the list of cars the user has saved/bookmarked.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the web for car reviews, reliability ratings, recalls, "
                "market pricing, or any other car-related information."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"],
            },
        },
    },
]


class CarScopeAgent:
    """
    Agent harness with 5 tool-style functions:
      1. list_current_cars    – what's on the current results page
      2. get_vehicle_details  – deep-dive on a specific car by ID
      3. compare_cars         – side-by-side comparison
      4. get_saved_cars       – user's saved list
      5. web_search           – DuckDuckGo lookup (no key required)

    Uses OpenAI function-calling when OPENAI_API_KEY is set,
    otherwise falls back to intent-based mock dispatch.
    """

    # ── Tool implementations ──────────────────────────────────────────────────

    @staticmethod
    def _list_current_cars(current_cars: List[Car]) -> Tuple[str, str]:
        if not current_cars:
            return "No cars are currently shown in the search results.", "0 cars on page"
        lines = [f"{len(current_cars)} car(s) on this page:"]
        for c in current_cars:
            trim = f" {c.trim}" if c.trim else ""
            lines.append(
                f"  • ID {c.id}: {c.year} {c.make} {c.model}{trim}"
                f" — ${c.price:,.0f}, {c.mileage:,} miles, {c.location}"
            )
        return "\n".join(lines), f"{len(current_cars)} cars listed"

    @staticmethod
    def _get_vehicle_details(car_id: str, pool: List[Car]) -> Tuple[str, str]:
        car = next((c for c in pool if str(c.id) == str(car_id)), None)
        if not car:
            return (
                f"Car with ID {car_id} was not found in the current page or saved cars.",
                f"Car {car_id} not found",
            )
        trim = f" {car.trim}" if car.trim else ""
        lines = [
            f"{car.year} {car.make} {car.model}{trim}",
            f"Price:    ${car.price:,.0f}",
            f"Mileage:  {car.mileage:,} miles",
            f"Location: {car.location}",
        ]
        if car.vin:
            lines.append(f"VIN:      {car.vin}")
        if car.description:
            lines.append(f"Notes:    {car.description}")
        lines.append(f"Source:   {car.source or 'local'}")
        return "\n".join(lines), f"{car.year} {car.make} {car.model} — ${car.price:,.0f}"

    @staticmethod
    def _compare_cars(car_ids: List[str], pool: List[Car]) -> Tuple[str, str]:
        cars = [c for c in pool if str(c.id) in [str(i) for i in car_ids]]
        if len(cars) < 2:
            return (
                "Could not find enough cars to compare. "
                "Make sure the car IDs are visible on the current page or in saved cars.",
                "Not enough matching cars",
            )
        headers = [f"{c.year} {c.make} {c.model}" for c in cars]
        col_w = max(len(h) for h in headers + ["Best $/mile"]) + 2

        def row(label: str, vals: List[str]) -> str:
            return f"{label:<14}" + "  ".join(v.ljust(col_w) for v in vals)

        lines = [
            row("", headers),
            row("Price",    [f"${c.price:,.0f}" for c in cars]),
            row("Mileage",  [f"{c.mileage:,} mi" for c in cars]),
            row("Year",     [str(c.year) for c in cars]),
            row("Location", [c.location for c in cars]),
            row("$/mile",   [
                f"${c.price / c.mileage:.2f}" if c.mileage > 0 else "N/A"
                for c in cars
            ]),
        ]
        cheapest = min(cars, key=lambda c: c.price)
        lowest_mi = min(cars, key=lambda c: c.mileage)
        best_val = min(cars, key=lambda c: c.price / c.mileage if c.mileage > 0 else float("inf"))
        lines += [
            "",
            f"Cheapest:     {cheapest.year} {cheapest.make} {cheapest.model} (${cheapest.price:,.0f})",
            f"Lowest miles: {lowest_mi.year} {lowest_mi.make} {lowest_mi.model} ({lowest_mi.mileage:,} mi)",
            f"Best $/mile:  {best_val.year} {best_val.make} {best_val.model}",
        ]
        return "\n".join(lines), f"Compared {len(cars)} cars"

    @staticmethod
    def _get_saved_cars(saved_cars: List[Car]) -> Tuple[str, str]:
        if not saved_cars:
            return "You have not saved any cars yet.", "No saved cars"
        by_price = sorted(saved_cars, key=lambda c: c.price)
        lines = [f"Your {len(saved_cars)} saved car(s) sorted by price:"]
        for c in by_price:
            lines.append(
                f"  • ID {c.id}: {c.year} {c.make} {c.model}"
                f" — ${c.price:,.0f}, {c.mileage:,} miles"
            )
        cheapest = by_price[0]
        lines.append(
            f"\nCheapest saved: {cheapest.year} {cheapest.make} {cheapest.model}"
            f" (${cheapest.price:,.0f})"
        )
        return "\n".join(lines), f"{len(saved_cars)} saved cars"

    @staticmethod
    async def _web_search(query: str) -> Tuple[str, str]:
        results = await web_search_tool(query)
        if not results:
            return (
                f"No results found for '{query}'. "
                "The DuckDuckGo instant-answer API may not have data for this specific query.",
                f"No results for '{query}'",
            )
        lines = [f'Web results for "{query}":']
        for r in results:
            if r.get("title"):
                lines.append(f"\n• {r['title']}")
            if r.get("snippet"):
                lines.append(f"  {r['snippet']}")
            if r.get("url"):
                lines.append(f"  {r['url']}")
        return "\n".join(lines), f"{len(results)} web result(s) for '{query}'"

    # ── Tool dispatcher ───────────────────────────────────────────────────────

    async def _call_tool(
        self,
        name: str,
        args: dict,
        current_car: Optional[Car],
        current_cars: List[Car],
        saved_cars: List[Car],
    ) -> Tuple[str, str]:
        # Unified pool deduplicates by ID
        seen: dict = {}
        for c in current_cars + saved_cars:
            seen[str(c.id)] = c
        pool = list(seen.values())

        if name == "list_current_cars":
            return self._list_current_cars(current_cars)
        if name == "get_vehicle_details":
            return self._get_vehicle_details(args.get("car_id", ""), pool)
        if name == "compare_cars":
            return self._compare_cars(args.get("car_ids", []), pool)
        if name == "get_saved_cars":
            return self._get_saved_cars(saved_cars)
        if name == "web_search":
            return await self._web_search(args.get("query", ""))
        return f"Unknown tool: {name}", f"Unknown: {name}"

    # ── Intent detection (mock mode) ──────────────────────────────────────────

    def _detect_intents(
        self,
        question: str,
        current_car: Optional[Car],
        current_cars: List[Car],
        saved_cars: List[Car],
    ) -> List[Tuple[str, dict]]:
        q = question.lower()
        calls: List[Tuple[str, dict]] = []

        # List page
        if re.search(r"(on|in) (this|the) page|current page|what cars|list.{0,8}cars|how many cars|show.{0,8}cars", q):
            calls.append(("list_current_cars", {}))

        # Saved cars
        if re.search(r"\bsaved\b|bookmark|my cars|favorites|favourites", q):
            calls.append(("get_saved_cars", {}))

        # Compare
        if "compare" in q:
            ids = re.findall(r"\b(\d+)\b", q)
            if len(ids) >= 2:
                calls.append(("compare_cars", {"car_ids": ids[:4]}))
            elif current_car and current_cars:
                others = [c for c in current_cars if str(c.id) != str(current_car.id)]
                partner = others[0] if others else (current_cars[1] if len(current_cars) > 1 else None)
                if partner:
                    calls.append(("compare_cars", {"car_ids": [str(current_car.id), str(partner.id)]}))
            elif len(current_cars) >= 2:
                calls.append(("compare_cars", {"car_ids": [str(c.id) for c in current_cars[:2]]}))

        # Specific car detail by ID mention
        id_match = re.search(r"(?:car|vehicle|id)\s+#?(\w+)", q)
        if id_match and "compare" not in q:
            calls.append(("get_vehicle_details", {"car_id": id_match.group(1)}))
        elif current_car and re.search(
            r"this car|this one|current car|is this|good option|good deal|worth it|tell me about", q
        ):
            calls.append(("get_vehicle_details", {"car_id": str(current_car.id)}))

        # Web search triggers
        if re.search(r"reliab|review|recall|issue|problem|pros|cons|worth|good deal|safety|rating", q):
            if current_car:
                web_q = f"{current_car.year} {current_car.make} {current_car.model} reliability review"
            elif current_cars:
                c = current_cars[0]
                web_q = f"{c.year} {c.make} {c.model} reliability review"
            else:
                web_q = question
            calls.append(("web_search", {"query": web_q}))
        elif re.search(r"search|look up|average price|market value|how much does|find info", q):
            calls.append(("web_search", {"query": question}))

        # Fallback
        if not calls:
            calls.append(("list_current_cars", {}))

        return calls

    # ── Response synthesis (mock mode) ────────────────────────────────────────

    @staticmethod
    def _synthesize(question: str, results: List[Tuple[str, dict, str]]) -> str:
        q = question.lower()
        body = "\n\n".join(f"[{name}]\n{text}" for name, _, text in results)

        if "compare" in q:
            return f"Here's the side-by-side comparison:\n\n{body}"
        if re.search(r"cheapest|lowest price|least expensive", q) and any(
            r[0] == "get_saved_cars" for r in results
        ):
            return f"From your saved cars:\n\n{body}"
        if re.search(r"good option|worth it|should i|good deal|recommend", q):
            return (
                f"Here's what I found to help you evaluate:\n\n{body}\n\n"
                "Consider the mileage-to-price ratio alongside any reliability data above."
            )
        return f"Here's what I found:\n\n{body}"

    # ── OpenAI loop ───────────────────────────────────────────────────────────

    async def _run_openai(
        self,
        question: str,
        system_prompt: str,
        current_car: Optional[Car],
        current_cars: List[Car],
        saved_cars: List[Car],
    ) -> AgentResult:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ]
        records: List[ToolCallRecord] = []

        for _ in range(6):  # max agent loop iterations
            resp = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )
            msg = resp.choices[0].message
            messages.append(msg.model_dump(exclude_none=True))

            if not msg.tool_calls:
                return AgentResult(answer=msg.content or "", tool_calls=records)

            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments or "{}")
                tool_result, summary = await self._call_tool(
                    tc.function.name, args, current_car, current_cars, saved_cars
                )
                records.append(ToolCallRecord(tool=tc.function.name, args=args, result_summary=summary))
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": tool_result})

        return AgentResult(
            answer="I wasn't able to complete the request after several attempts.",
            tool_calls=records,
        )

    # ── Mock loop ─────────────────────────────────────────────────────────────

    async def _run_mock(
        self,
        question: str,
        current_car: Optional[Car],
        current_cars: List[Car],
        saved_cars: List[Car],
    ) -> AgentResult:
        intents = self._detect_intents(question, current_car, current_cars, saved_cars)
        records: List[ToolCallRecord] = []
        results: List[Tuple[str, dict, str]] = []

        for tool_name, args in intents:
            text, summary = await self._call_tool(tool_name, args, current_car, current_cars, saved_cars)
            records.append(ToolCallRecord(tool=tool_name, args=args, result_summary=summary))
            results.append((tool_name, args, text))

        return AgentResult(answer=self._synthesize(question, results), tool_calls=records)

    # ── Public entry point ────────────────────────────────────────────────────

    async def run(
        self,
        question: str,
        current_car: Optional[Car],
        current_cars: List[Car],
        saved_cars: List[Car],
    ) -> AgentResult:
        api_key = os.getenv("OPENAI_API_KEY", "")
        use_openai = api_key not in ("", "your_api_key_here")

        if use_openai:
            ctx_parts = [
                "You are CarScope AI, an expert car shopping assistant.",
                "Use tools to fetch accurate data before answering.",
                "Always cite specific cars by their IDs.",
            ]
            if current_cars:
                ctx_parts.append(f"The search page shows {len(current_cars)} car(s).")
            if current_car:
                ctx_parts.append(
                    f"The user is currently viewing: "
                    f"{current_car.year} {current_car.make} {current_car.model} (ID {current_car.id})."
                )
            if saved_cars:
                ctx_parts.append(f"The user has {len(saved_cars)} saved car(s).")
            try:
                return await self._run_openai(
                    question, " ".join(ctx_parts), current_car, current_cars, saved_cars
                )
            except Exception:
                pass  # fall through to mock on any error

        return await self._run_mock(question, current_car, current_cars, saved_cars)
