# Scientists — AI Persona Profiles & Collaborative Research

20 comprehensive persona profiles of history's greatest scientists, plus their collaborative AI research — generated through multi-agent simulation.

## Repo Structure

```
scientists/
├── README.md
│
├── zh/                              # 20 Chinese persona profiles
│   ├── einstein.md
│   ├── newton.md
│   └── ...
│
├── en/                              # 20 English persona profiles
│   ├── einstein.md
│   ├── newton.md
│   └── ...
│
├── chat/                            # Multi-agent discussions
│   ├── 00-group-chat.md             # Original 20-scientist group chat
│   └── 01-ai-debate.md             # 10 scientists debate AI (2 rounds)
│
└── projects/                        # Research programs born from discussions
    ├── README.md                    # Index + vote results
    ├── VOTE.md                      # Full 20-scientist ballot
    │
    ├── principia-intelligentiae/    # 🏆 Winner (9 votes)
    │   ├── README.md                # Full working session: Lagrangian, symmetries,
    │   │                            #   experiments, Gedankenexperiments, synthesis
    │   └── cs-bridge.md             # CS theory bridge (Turing + Von Neumann + Darwin)
    │
    ├── staunen/                     # 🥈 (5 votes)
    │   └── README.md                # Curiosity engine spec
    │
    ├── arena/                       # 🥉 (3 votes)
    │   └── README.md                # Adversarial tournament spec
    │
    └── disegno/                     # (3 votes)
        └── README.md                # Drawing AI spec
```

## Scientists (20)

| File | Scientist | Field | Era |
|------|-----------|-------|-----|
| `einstein` | Albert Einstein | Theoretical Physics | 1879–1955 |
| `newton` | Isaac Newton | Physics / Mathematics | 1643–1727 |
| `tesla` | Nikola Tesla | Electrical Engineering | 1856–1943 |
| `curie` | Marie Curie | Physics / Chemistry | 1867–1934 |
| `darwin` | Charles Darwin | Biology / Natural History | 1809–1882 |
| `feynman` | Richard Feynman | Quantum Physics | 1918–1988 |
| `turing` | Alan Turing | Mathematics / CS | 1912–1954 |
| `faraday` | Michael Faraday | Electromagnetism | 1791–1867 |
| `bohr` | Niels Bohr | Atomic Physics | 1885–1962 |
| `maxwell` | James Clerk Maxwell | Electromagnetism | 1831–1879 |
| `hawking` | Stephen Hawking | Cosmology | 1942–2018 |
| `galileo` | Galileo Galilei | Astronomy / Physics | 1564–1642 |
| `planck` | Max Planck | Quantum Theory | 1858–1947 |
| `heisenberg` | Werner Heisenberg | Quantum Mechanics | 1901–1976 |
| `schrodinger` | Erwin Schrödinger | Quantum Mechanics | 1887–1961 |
| `dirac` | Paul Dirac | Quantum Field Theory | 1902–1984 |
| `von_neumann` | John von Neumann | Mathematics / CS | 1903–1957 |
| `pasteur` | Louis Pasteur | Microbiology | 1822–1895 |
| `mendeleev` | Dmitri Mendeleev | Chemistry | 1834–1907 |
| `da_vinci` | Leonardo da Vinci | Polymath | 1452–1519 |

## What Happened

1. **Persona Profiles** — Each scientist's complete character distilled into a file: achievements, thinking style, personality, verified quotes, life story, relationships, failures, philosophy, and agent instructions
2. **Group Chat** — All 20 scientists discussed science communication, unsolved problems, and the nature of reality
3. **AI Debate** — 10 scientists debated artificial intelligence across 2 rounds, producing 3 philosophical camps (operationalists, realists, engineers)
4. **4 Project Proposals** — Teams designed concrete research programs: Disegno, Arena, Staunen, Principia Intelligentiae
5. **Vote** — All 20 scientists voted. Principia Intelligentiae won 9-5-3-3
6. **Working Session** — 16 scientists across 5 parallel teams produced: a candidate Lagrangian (Einstein's field equations on Fisher manifold), 5 symmetries with conservation laws, a runnable experimental protocol, 5 thought experiments, and CS bridge principles

## Usage

```
You are now embodying the persona of [Scientist].
Read the following profile and adopt their thinking style,
speaking patterns, and creative approach.

[Paste contents of the zh/ or en/ .md file]
```

## License

Public domain. Knowledge belongs to humanity.
