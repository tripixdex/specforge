# SpecForge

Локальный детерминированный инструмент, который преобразует неструктурированные продуктовые описания в структурированный анализ, сигналы для планирования и поставочный комплект внутри репозитория.

## Зачем это нужно

SpecForge сильнее всего смотрится как портфолио-проект, если воспринимать его как рабочий процесс перехода от неопределенности к структуре: взять недостаточно проработанное описание, выявить неясные или противоречивые места и подготовить артефакты, которые делают следующий продуктовый разговор точнее.

## Возможности

- Детерминированный конвейер приема, анализа, генерации и экспорта
- Анализ неоднозначностей, противоречий, отсутствующих решений и допущений на основе правил
- CLI, FastAPI API, браузерный интерфейс и встроенный демонстрационный сценарий
- Экспортные комплекты внутри репозитория в `outputs/`
- Оценочный набор с 26 локальными случаями и структурными проверками
- Английские и русские результаты, соответствующие языку входных данных

## Быстрая демонстрация

Установка из локальной копии исходного кода:

```bash
python3 -m pip install --no-build-isolation -e ".[dev]"
```

Самый короткий демонстрационный путь:

```bash
python3 -m specforge.cli demo
```

Демонстрация в браузере:

```bash
python3 -m uvicorn specforge.api.app:app --host 127.0.0.1 --port 8000
```

Затем откройте `http://127.0.0.1:8000/ui`.

Полезные примеры CLI:

```bash
python3 -m specforge.cli analyze --input examples/contradictory_founder_brief.txt
python3 -m specforge.cli generate --input examples/internal_operations_tool_brief.txt
```

## Проверка

Легкий путь проверки для этого репозитория:

```bash
make lint
python3 -m pytest tests/test_api.py -q
python3 -m specforge.cli demo
python3 -m specforge.eval.runner --case-id internal_clear_local_tool
```

Он проверяет стиль, поведение API, основной путь формирования демонстрационного комплекта и один сфокусированный оценочный случай без запуска широкого цикла аудита.

## Демонстрационная поверхность

- `GET /health`
- `GET /demo`
- `POST /analyze`
- `POST /generate`
- `GET /`
- `GET /ui`

Интерфейс и API сохраняют сгенерированные комплекты в [outputs/](/Users/vladgurov/Desktop/work/specforge/outputs). Браузерный сценарий не загружает файлы наружу и не позволяет задавать произвольные пути экспорта.

## Ограничения

- Это локальное демонстрационное программное обеспечение, а не размещенная продуктовая платформа планирования
- Анализ детерминированный и основан на правилах; он не заменяет работу с заинтересованными сторонами
- Нет аутентификации, совместной работы, облачного развертывания и внешних интеграций
- Экспорт из API и интерфейса по замыслу остается внутри репозитория
- Качество результата зависит от того, содержит ли исходное описание достаточно конкретных деталей для рассуждения

## Почему это интересно в портфолио

Этот репозиторий показывает продуктовые механики в коде: проверку входных данных, детерминированный анализ, поставку через несколько поверхностей, проверяемые артефакты и честно обозначенные границы того, что автоматизация может и не может вывести.

## Примеры входных данных и артефактов

Примеры описаний находятся в [examples/founder_app_idea.txt](/Users/vladgurov/Desktop/work/specforge/examples/founder_app_idea.txt), [examples/contradictory_founder_brief.txt](/Users/vladgurov/Desktop/work/specforge/examples/contradictory_founder_brief.txt), [examples/agency_client_brief.txt](/Users/vladgurov/Desktop/work/specforge/examples/agency_client_brief.txt) и [examples/internal_operations_tool_brief.txt](/Users/vladgurov/Desktop/work/specforge/examples/internal_operations_tool_brief.txt).

Самый сильный существующий демонстрационный комплект: [outputs/demo-founder-app/analysis_report.md](/Users/vladgurov/Desktop/work/specforge/outputs/demo-founder-app/analysis_report.md) и связанные файлы в [outputs/demo-founder-app](/Users/vladgurov/Desktop/work/specforge/outputs/demo-founder-app).

## Документация

- [docs/DEMO_SCENARIOS.md](/Users/vladgurov/Desktop/work/specforge/docs/DEMO_SCENARIOS.md)
- [docs/ARCHITECTURE.md](/Users/vladgurov/Desktop/work/specforge/docs/ARCHITECTURE.md)
- [docs/SCOPE.md](/Users/vladgurov/Desktop/work/specforge/docs/SCOPE.md)
- [docs/EVAL_PLAN.md](/Users/vladgurov/Desktop/work/specforge/docs/EVAL_PLAN.md)
