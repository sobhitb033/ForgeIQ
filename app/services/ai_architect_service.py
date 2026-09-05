import json
import re
from typing import Any

import httpx


class AIArchitectService:
    """Generate structured architecture guidance from ForgeIQ's deterministic analysis."""

    @staticmethod
    def build_context(snapshot: dict[str, Any]) -> dict[str, Any]:
        health = snapshot.get("project_health", {}) or {}
        architecture = snapshot.get("architecture", {}) or {}
        graph = snapshot.get("graph_analysis", {}) or {}
        summary = snapshot.get("summary", {}) or {}
        recommendations = snapshot.get("recommendations", []) or []
        files = snapshot.get("files", []) or []

        file_context = []
        for item in files:
            metrics = item.get("metrics", {}) or {}
            maintainability = item.get("maintainability", {}) or {}
            priority = item.get("engineering_priority", {}) or {}
            impact = item.get("module_impact", {}) or {}
            smells = item.get("code_smells", []) or []

            file_context.append({
                "file": item.get("file"),
                "metrics": {
                    "code_lines": metrics.get("code_lines", 0),
                    "classes": metrics.get("classes", 0),
                    "functions": metrics.get("functions", 0),
                    "methods": metrics.get("methods", 0),
                    "imports": metrics.get("imports", 0),
                },
                "maintainability": maintainability,
                "engineering_priority": priority,
                "module_impact": impact,
                "code_smells": [
                    {
                        "type": smell.get("type"),
                        "severity": smell.get("severity"),
                        "location": smell.get("location"),
                        "message": smell.get("message"),
                    }
                    for smell in smells[:8]
                ],
            })

        file_context.sort(
            key=lambda item: (
                -float((item.get("engineering_priority") or {}).get("score", 0) or 0),
                item.get("file") or "",
            )
        )

        return {
            "project_summary": summary,
            "project_health": health,
            "architecture": architecture,
            "dependency_graph_analysis": {
                "circular_dependencies": graph.get("circular_dependencies", []),
                "nodes": graph.get("nodes", []),
                "edges": graph.get("edges", []),
            },
            "recommendations": recommendations[:15],
            "files": file_context[:60],
        }

    @staticmethod
    def _resolve_focus(snapshot: dict[str, Any], focus: dict[str, Any] | None) -> dict[str, Any] | None:
        if not focus or not focus.get("target"):
            return None

        target = str(focus.get("target") or "").strip()
        kind = str(focus.get("kind") or "module").strip().lower()
        normalized = target.replace("\\", "/")
        module_target = normalized[:-3].replace("/", ".") if normalized.endswith(".py") else normalized.replace("/", ".")

        files = snapshot.get("files", []) or []
        matched = []
        for item in files:
            file_name = str(item.get("file") or "")
            file_norm = file_name.replace("\\", "/")
            file_module = file_norm[:-3].replace("/", ".") if file_norm.endswith(".py") else file_norm.replace("/", ".")
            if target == file_name or normalized == file_norm or target == file_module or module_target == file_module:
                matched.append(item)

        result: dict[str, Any] = {
            "kind": kind,
            "target": target,
            "title": focus.get("title"),
        }

        if matched:
            item = matched[0]
            result["file"] = item.get("file")
            result["metrics"] = item.get("metrics", {})
            result["maintainability"] = item.get("maintainability", {})
            result["engineering_priority"] = item.get("engineering_priority", {})
            result["module_impact"] = item.get("module_impact", {})
            result["dependencies"] = item.get("dependencies", {})
            smells = item.get("code_smells", []) or []
            smell_type = str(focus.get("smell_type") or "").strip().lower()
            if kind == "smell" and smell_type:
                result["selected_smells"] = [
                    x for x in smells
                    if str(x.get("type") or "").strip().lower() == smell_type
                ][:5]
            else:
                result["code_smells"] = smells[:5]

        if kind == "recommendation":
            recommendations = snapshot.get("recommendations", []) or []
            result["recommendation"] = next(
                (x for x in recommendations if str(x.get("title") or "").strip() == target),
                None,
            )

        architecture = snapshot.get("architecture", {}) or {}
        core_modules = architecture.get("core_modules", []) or []
        result["core_module"] = next(
            (x for x in core_modules if str(x.get("module") or "").strip() == target),
            None,
        )
        result["matched"] = bool(matched or result.get("recommendation") or result.get("core_module"))
        return result

    @staticmethod
    def _build_prompt(
        context: dict[str, Any],
        question: str | None = None,
        history: list[dict[str, str]] | None = None,
        focus: dict[str, Any] | None = None,
    ) -> str:
        question_text = question.strip() if question and question.strip() else (
            "Give the most important architectural assessment and a practical refactoring plan for this project."
        )

        conversation = []
        for item in (history or [])[-8:]:
            role = item.get("role")
            content = str(item.get("content") or "").strip()
            if role in {"user", "assistant"} and content:
                conversation.append({"role": role, "content": content[:4000]})

        schema = {
            "executive_assessment": "2-4 concise sentences",
            "top_risks": [
                {
                    "title": "short risk name",
                    "severity": "Critical | High | Medium",
                    "evidence": "specific observed facts with real module names/metrics",
                    "why_it_matters": "concise architectural impact",
                    "recommended_action": "concrete next action",
                }
            ],
            "refactoring_order": [
                {
                    "phase": "Phase 1",
                    "title": "short action",
                    "action": "specific refactoring action",
                }
            ],
            "quick_wins": ["short actionable item"],
            "structural_changes": ["short architectural change"],
            "manual_investigation": ["specific thing to verify before risky changes"],
        }

        focus_context = focus or {}

        return f"""You are ForgeIQ's AI Software Architect.

ForgeIQ has already performed deterministic static analysis. Treat the supplied analysis as the source of truth. Never invent files, dependencies, metrics, layers, code smells, or problems.

The user wants an engineering decision, not a generic code-quality lecture. Prefer architectural impact, dependency structure, blast radius, maintainability, complexity, and existing ForgeIQ recommendations over cosmetic advice.

Distinguish internally between observed facts and architectural inferences. Only state an observed fact when it is supported by the supplied analysis. If something is an inference, phrase it as an inference.

Return ONLY valid JSON. Do not use Markdown fences. Use exactly this shape:
{json.dumps(schema, indent=2)}

Rules:
- top_risks: maximum 5; use 3 when the evidence is strong enough.
- refactoring_order: maximum 5 phases, ordered by architectural impact and dependency risk.
- quick_wins: maximum 5.
- structural_changes: maximum 4.
- manual_investigation: maximum 4.
- Keep every string concise: normally 1-3 sentences.
- Use actual module/file names and metrics when available.
- Do not repeat the same point across multiple sections unless necessary.
- If the analysis does not support a claim, omit it.
- Use the conversation history only to resolve follow-up references such as "why", "that module", or "the second risk".
- Do not treat previous assistant statements as evidence; the ForgeIQ analysis context remains the source of truth.
- Answer the current user request directly; do not repeat the entire previous assessment unless needed.
- If a selected UI focus is supplied, answer about that target first. The selected-focus facts below are derived from the same ForgeIQ snapshot; if they conflict with any user wording, trust the snapshot-derived facts.

Conversation history:
{json.dumps(conversation, indent=2, default=str)}

User request:
{question_text}

Selected ForgeIQ UI focus:
{json.dumps(focus_context, indent=2, default=str)}

ForgeIQ analysis context:
{json.dumps(context, indent=2, default=str)}
"""

    @staticmethod
    def _clean_json_text(content: str) -> str:
        text = content.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
        return text.strip()

    @staticmethod
    def _fallback(content: str) -> dict[str, Any]:
        return {
            "executive_assessment": content.strip(),
            "top_risks": [],
            "refactoring_order": [],
            "quick_wins": [],
            "structural_changes": [],
            "manual_investigation": [],
        }

    @classmethod
    def normalize_response(cls, content: str) -> dict[str, Any]:
        cleaned = cls._clean_json_text(content)
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            return cls._fallback(content)

        if not isinstance(parsed, dict):
            return cls._fallback(content)

        result = {
            "executive_assessment": str(parsed.get("executive_assessment") or "").strip(),
            "top_risks": parsed.get("top_risks") if isinstance(parsed.get("top_risks"), list) else [],
            "refactoring_order": parsed.get("refactoring_order") if isinstance(parsed.get("refactoring_order"), list) else [],
            "quick_wins": parsed.get("quick_wins") if isinstance(parsed.get("quick_wins"), list) else [],
            "structural_changes": parsed.get("structural_changes") if isinstance(parsed.get("structural_changes"), list) else [],
            "manual_investigation": parsed.get("manual_investigation") if isinstance(parsed.get("manual_investigation"), list) else [],
        }

        result["top_risks"] = [x for x in result["top_risks"] if isinstance(x, dict)][:5]
        result["refactoring_order"] = [x for x in result["refactoring_order"] if isinstance(x, dict)][:5]
        result["quick_wins"] = [str(x).strip() for x in result["quick_wins"] if str(x).strip()][:5]
        result["structural_changes"] = [str(x).strip() for x in result["structural_changes"] if str(x).strip()][:4]
        result["manual_investigation"] = [str(x).strip() for x in result["manual_investigation"] if str(x).strip()][:4]

        if not result["executive_assessment"]:
            result["executive_assessment"] = "ForgeIQ returned an architectural assessment, but no executive summary was provided."
        return result

    @classmethod
    async def analyze(
        cls,
        snapshot: dict[str, Any],
        api_key: str,
        base_url: str,
        model: str,
        question: str | None = None,
        history: list[dict[str, str]] | None = None,
        focus: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        context = cls.build_context(snapshot)
        resolved_focus = cls._resolve_focus(snapshot, focus)
        prompt = cls._build_prompt(context, question, history, resolved_focus)
        url = base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a senior software architect inside ForgeIQ. Return valid JSON only and never fabricate analysis facts.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.15,
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        import asyncio

        def _request_provider() -> httpx.Response:
            last_error: Exception | None = None
            for attempt in range(3):
                try:
                    with httpx.Client(timeout=90.0, trust_env=False) as client:
                        return client.post(url, headers=headers, json=payload)
                except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadError, httpx.NetworkError) as exc:
                    last_error = exc
                    if attempt < 2:
                        import time
                        time.sleep(0.5 * (attempt + 1))
            raise RuntimeError(f"Unable to reach AI provider after 3 attempts: {last_error}") from last_error

        response = await asyncio.to_thread(_request_provider)

        if response.status_code >= 400:
            detail = response.text[:1000]
            raise RuntimeError(f"AI provider returned HTTP {response.status_code}: {detail}")

        data = response.json()
        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError("AI provider returned no response choices.")

        message = choices[0].get("message") or {}
        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("AI provider returned an empty response.")

        return cls.normalize_response(content)
