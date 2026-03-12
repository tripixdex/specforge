"""Localized UI copy for the server-rendered browser flow."""

from __future__ import annotations

from specforge.pipeline.language import Locale


def ui_strings(locale: Locale) -> dict[str, str]:
    """Return lightweight localized browser copy."""

    if locale == "ru":
        return {
            "eyebrow": "SpecForge Stage 5.7",
            "page_title": "SpecForge: локальный анализ брифов",
            "hero_title": "Локальный анализ брифов в спокойном пошаговом интерфейсе",
            "hero_copy": (
                "Вставьте сырой бриф, загрузите демо-пример, посмотрите риски планирования "
                "и соберите локальный пакет артефактов. Все работает локально, детерминированно "
                "и без LLM."
            ),
            "step_intake": "1. Ввод",
            "step_analysis": "2. Анализ",
            "step_generation": "3. Генерация",
            "brief_input": "Бриф",
            "brief_input_copy": "Загрузите демо или вставьте свой локальный бриф.",
            "bundled_demo": "Демо-пример",
            "load_demo": "Загрузить демо",
            "title": "Название",
            "title_placeholder": "Необязательное название брифа",
            "brief_text": "Сырой бриф",
            "brief_placeholder": "Вставьте сюда исходный текст брифа",
            "output_label": "Метка вывода",
            "output_placeholder": "Необязательная метка папки внутри outputs/",
            "generate_bundle": "Сгенерировать пакет",
            "run_analysis": "Запустить анализ",
            "start_over": "Новый бриф",
            "form_note": "Пакеты из UI всегда остаются внутри outputs/.",
            "results": "Результаты",
            "results_copy": "Сначала главное, затем детали и артефакты.",
            "count_ambiguities": "Неясности",
            "count_contradictions": "Противоречия",
            "count_missing_decisions": "Недостающие решения",
            "count_assumptions": "Допущения",
            "input_issue": "Проблема со вводом",
            "brief_summary": "Краткое резюме",
            "open_questions": "Открытые вопросы",
            "unresolved": "Нужно решить",
            "recommended_mvp_cut": "Рекомендуемый MVP",
            "ambiguity_findings": "Неясности",
            "contradictions": "Противоречия",
            "high_risk": "Высокий риск",
            "missing_decisions": "Недостающие решения",
            "assumptions": "Допущения",
            "generated_bundle": "Сгенерированный пакет",
            "repo_local": "Локально в репозитории",
            "bundle_path": "Путь к пакету",
            "show_full_path": "Показать полный путь",
            "artifacts": "Артефакты",
            "artifact_kind_markdown": "markdown",
            "artifact_kind_json": "json",
            "evidence_label": "Основания",
            "start_with_analysis": "Начните с анализа",
            "start_with_analysis_copy": (
                "Загрузите демо или вставьте свой бриф, затем запустите анализ, чтобы увидеть "
                "резюме, вопросы, риски и рекомендации."
            ),
            "no_contradictions": "Противоречий не обнаружено.",
            "no_ambiguities": "Неясности не обнаружены.",
            "no_missing_decisions": "Недостающих решений не обнаружено.",
            "no_assumptions": "Допущения не добавлены.",
            "no_open_questions": "Открытых вопросов нет.",
            "no_mvp_cut": "Рекомендация по MVP пока не сформирована.",
            "no_artifacts": "Артефакты появятся после генерации пакета.",
            "needs_more_detail": "Нужно чуть больше контекста",
            "needs_more_detail_copy": (
                "Этот бриф пока слишком короткий для уверенного объема. "
                "Сначала уточните самые важные опоры."
            ),
            "clarify_first": "Сначала уточните",
            "severity_high": "высокий",
            "severity_medium": "средний",
            "severity_low": "низкий",
            "reset_note": (
                "Новый бриф очищает текст, название и результаты, "
                "но оставляет демо-выбор доступным."
            ),
        }
    return {
        "eyebrow": "SpecForge Stage 5.7",
        "page_title": "SpecForge: local brief analysis",
        "hero_title": "Local brief analysis in a calm guided workflow",
        "hero_copy": (
            "Paste a messy brief, load a demo brief, inspect planning risks, and "
            "generate a local artifact bundle. Everything stays local, deterministic, "
            "and free of LLM shortcuts."
        ),
        "step_intake": "1. Intake",
        "step_analysis": "2. Analysis",
        "step_generation": "3. Generation",
        "brief_input": "Brief input",
        "brief_input_copy": "Load a demo or paste your own local brief.",
        "bundled_demo": "Bundled demo",
        "load_demo": "Load demo",
        "title": "Title",
        "title_placeholder": "Optional brief title",
        "brief_text": "Messy brief",
        "brief_placeholder": "Paste the raw brief text here",
        "output_label": "Output label",
        "output_placeholder": "Optional folder label under outputs/",
        "generate_bundle": "Generate bundle",
        "run_analysis": "Run analysis",
        "start_over": "New brief",
        "form_note": "Bundles from the UI always stay under outputs/.",
        "results": "Guided results",
        "results_copy": "Core meaning first, details and artifacts second.",
        "count_ambiguities": "Ambiguities",
        "count_contradictions": "Contradictions",
        "count_missing_decisions": "Missing decisions",
        "count_assumptions": "Assumptions",
        "input_issue": "Input issue",
        "brief_summary": "Brief summary",
        "open_questions": "Open questions",
        "unresolved": "Unresolved",
        "recommended_mvp_cut": "Recommended MVP cut",
        "ambiguity_findings": "Ambiguity findings",
        "contradictions": "Contradictions",
        "high_risk": "High risk",
        "missing_decisions": "Missing decisions",
        "assumptions": "Assumptions",
        "generated_bundle": "Generated bundle",
        "repo_local": "Repo-local",
        "bundle_path": "Bundle path",
        "show_full_path": "Show full path",
        "artifacts": "Artifacts",
        "artifact_kind_markdown": "markdown",
        "artifact_kind_json": "json",
        "evidence_label": "Evidence",
        "start_with_analysis": "Start with analysis",
        "start_with_analysis_copy": (
            "Load a demo or paste your own brief, then run analysis to see the summary, "
            "open questions, risk signals, and MVP guidance."
        ),
        "no_contradictions": "No contradictions detected.",
        "no_ambiguities": "No ambiguity findings.",
        "no_missing_decisions": "No missing decisions detected.",
        "no_assumptions": "No assumptions were added.",
        "no_open_questions": "No open questions were generated.",
        "no_mvp_cut": "No MVP cut recommendation was generated.",
        "no_artifacts": "Artifacts will appear after bundle generation.",
        "needs_more_detail": "Need a bit more detail",
        "needs_more_detail_copy": (
            "This brief is still too short for a confident scope draft. "
            "Start with the missing essentials first."
        ),
        "clarify_first": "Clarify first",
        "severity_high": "high",
        "severity_medium": "medium",
        "severity_low": "low",
        "reset_note": (
            "New brief clears the current text, title, output label, and results, "
            "while keeping demo selection available."
        ),
    }
