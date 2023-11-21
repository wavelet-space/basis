# essence

![main](https://github.com/czech-radio/essence/workflows/main/badge.svg)

**Tiny WSGI framework to speedup a microservice development with help of domain-driven design and clean architecture.**

## Motivation & Features

[cs]
- Maximálně zjedodušit vytváření nových projektů pomocí předpřipravených šablon.
- Vytvořit dobrý a kompletní doménový model, ne jako většina frameworků, které jsou kolekcí ad-hoc tříd a funkcí.
- Možnost vytvořit web aplikaci, API, CLI, jen omocí jednoho příkazu.
- Aplikace bude mít automaticky vygenerovanou dokumentaci a strukturní diagramy.
- Aplikace bude mít automaticky vygenerovanou konfiguraci a  bude ji možné uhned spouštět v kontejneru.

## Installation & Usage

```
py 3.9 -m venv .venv
.venv\Scripts\activate
pip install ".[lint, test]"
pytest
```

## Development

### Requirements

- Git
- GiHub
- Python 3.8+
- VSCode

### Structure

```shell
$ tree -I '.mypy_cache|.pytest_cache|.venv|*.egg-info|__pycache__'
```

## Roadmap

- [ ] Implement and document the basic blocks of Domain Driven Design (DDD)
  - Factories for aggregates / Factory pattern
  - Repositories for aggregates / Repository pattern
  - Domain model: Events, Entitites, Values (Value objects)
  - Application services
  - Predicates/Specification pattern
  - Validation

- [ ] Implement the application facade as interface and create example how to run the application as
  - Flask REST application
  - Command line application

- [ ] Compare Clean Architecture (CA) and Domain Driven Design (DDD)

- [ ] Overview of SAM pattern

## License MIT

See the [`LICENSE`](ttps://github.com/wavelet-space/ringen/LICENSE) file.
