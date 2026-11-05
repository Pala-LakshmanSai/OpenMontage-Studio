# Install this production setup

Open `https://github.com/Pala-LakshmanSai/OpenMontage-Studio` in Codex and say:

> Install OpenMontage from this repository, including my authorized private API
> setup. Read its agent guide and production knowledge. Set it up for this computer,
> verify the saved styles and tools, and preserve existing configuration and work.

To clone manually: `git clone https://github.com/Pala-LakshmanSai/OpenMontage-Studio.git`.
Then open that folder in Codex. The public source needs no private GitHub login.

The installer is `python scripts/install_openmontage.py --with-private-config`.
On Windows use `py -3 scripts/install_openmontage.py --with-private-config`.
It creates/reuses `.venv`, installs Python dependencies and the Remotion composer,
and downloads the owner-authorized private setup asset through authenticated
GitHub CLI. Keys live in ignored local files, never in logs or shared training.
For the optional private download, the friend must have access to the private
`Pala-LakshmanSai/OpenMontage` setup repository and authenticate `gh`;
the install cannot grant itself access. Alternatively provide a local setup ZIP
and use `--private-config /path/to/OpenMontage-Private-API-Setup.zip`, avoiding
individual key entry and private GitHub access. The private setup asset intentionally
grants the repository's authorized readers access to the configured provider keys.

Python 3.10+, Node/npm, FFmpeg/ffprobe, Git and GitHub CLI must be available.
Python 3.12 is the tested production baseline and uses the shipped dependency
constraints matching the owner's working environment. Other supported Python
versions resolve compatible packages and need their own capability check.
An installing agent should resolve missing system prerequisites through the
platform's supported package manager, using ordinary installation authorization.
Do not purchase providers or activate subscriptions. Run the installer again
afterward; it fails clearly rather than reporting a partial setup as ready.
It preserves an existing `.env` and adds only missing empty variables. Refreshing
existing credentials requires `--refresh-private-config` and keeps a local backup.

Check without installing or making provider calls:

```sh
python scripts/install_openmontage.py --check
python scripts/check_production_knowledge.py
```

After installation, a production prompt can be:

> Make a 20-minute video in Primitive Desert Style titled [TITLE]. Follow the
> saved training, reuse this project's selected cast/world where available, use
> my authorized active Frameo unlimited plan, and finish and show the full video.

Other saved names: AI Movies, Vlog Style, AI Videos Documentary Style, Outdoor
Boys Style, Tech Trendy Style and **The Last Day**. For the latter, title plus
duration invokes the saved narrated science/disaster workflow, including its
pilot-derived editorial playbook; no personal Codex memory or reference downloads
are required. For example: “The Last Day: [TITLE], around 10 minutes.”
New styles inherit the shared policies and get
their own guide, reference notes, template and playbook where appropriate.
For **Queen Elizabeth I Style**, the knowledge index also discovers its detailed
production playbook and one copyable Claude prompt. Paste
`docs/queen-elizabeth-i-claude-story-prompt.md` once in a Claude Project with the
reference channel links, retain its evidence and style bible there, then supply
a title and approximate duration for each story. Queen Elizabeth I is the primary
historical-insider format;
Chloe VS History supplies explicitly selected secondary lessons rather than an
automatic blended persona. Copy these regular repository files or update normally;
personal Codex memory and the original Mac's drive paths are not required.
The active title, length, cast, budget and account entitlement remain real inputs;
old project approval or an expired pass does not authorize a new paid production.

## Updates

Before a new production on an installed public checkout, check for a repository
update once while idle. If clean and safely fast-forwardable, update and run the
knowledge check automatically; install changed dependencies when needed. Preserve
local edits and all production assets. Do not update an active worker's source.
This carries new saved teachings into subsequent video requests without making
the friend ask for or repeat them. An offline check uses the installed training
and reports its version when relevant rather than blocking independent work.

The owner's scheduled publisher checks for durable new preferences and completed
source changes, validates them, and pushes a normal commit to the public source repo.
It does not publish raw chats, credentials, production media or unfinished jobs.
New secrets are delivered through the separate private `owner-private-setup`
release asset `openmontage-private-setup.zip`, not ordinary preference commits.

The publisher is scheduled hourly on the owner's Codex desktop, named
“Update OpenMontage public production repo”. It stays quiet without meaningful
changes. Scheduled execution requires that desktop environment to be available;
it is not an always-on GitHub server service.

On the friend's computer, say “Update OpenMontage and install any new requirements.”
The agent reads this guide, checks local changes and running work, uses a normal
fast-forward pull when safe, reruns installation and the knowledge check, and
retains all local projects/keys. No reset, clean, force-push or overwrite to make an
update succeed. A divergent checkout gets an isolated merge/update with conflicts
resolved while preserving local work. Never pull over a live generation worker.

The repo transfers the standards, supported tools and workflow. It does not copy
Codex subscriptions, authenticated browser sessions, provider entitlements or
external media referenced by symlinks. Required cast/voice/world assets must be
copied explicitly for a continuation; new productions can establish new original
references. The original cast is never silently replaced. Hardware, network,
provider queues and stochastic outputs affect speed and quality on each device.
