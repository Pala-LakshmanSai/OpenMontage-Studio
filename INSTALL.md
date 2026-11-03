# Install the trained OpenMontage setup

Public source: https://github.com/Pala-LakshmanSai/OpenMontage-Studio

Open this repository in Codex and say:

> Install this project, including my authorized private API setup. Read the saved
> production knowledge and verify all styles are available on this computer.

Follow [installation and updates](docs/install-and-update.md). The agent starts
at [AGENT_GUIDE.md](AGENT_GUIDE.md), loads the [style/policy index](docs/production-knowledge-index.json),
and installs with `python scripts/install_openmontage.py --with-private-config`
(Windows: `py -3 scripts/install_openmontage.py --with-private-config`).

Public source includes the training and tools. Owner-provided API configuration
installs from a separately supplied private setup ZIP with `--private-config`,
or from the owner’s private setup repository with authenticated GitHub CLI. No paid
generation, credit purchase or subscription activation is part of installation.

Then request a style, title and length. The saved storytelling, continuity,
performance, sound, production-speed and delivery rules load from the repository;
the original owner's personal memory and earlier chats are not required.
