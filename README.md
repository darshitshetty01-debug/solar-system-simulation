# Solar System Simulation

A simple simulation of the six classical planets (Mercury through Saturn) orbiting the Sun, built in Python using `qdraw.py` — a custom `turtle`-based drawing module written by Mark Newman.

## Features

- Circle sizes and orbital radii scaled from real planet data, compressed for visual clarity (the true ratios between inner and outer planets are too extreme to fit on screen)
- Orbital speeds scaled relative to Mercury (`omega = T_mercury / T_planet`)
- White trails showing each planet's path

## Files

- `solar_system.py` — main simulation script
- `qdraw.py` — drawing module (by Mark Newman, Revised BSD License)

## Requirements

- Python 3
- `numpy`

## Running it

\`\`\`bash
python solar_system.py
\`\`\`

## License

This project's code (`solar_system.py`) is licensed under the MIT License — see [LICENSE](LICENSE).

`qdraw.py` is included as a dependency and retains its own Revised BSD License and copyright, held by Mark Newman.