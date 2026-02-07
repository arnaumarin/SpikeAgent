<p align="center">
  <img src="docs/spikeagent_logo.png" alt="SpikeAgent Logo" width="300">
</p>

# SpikeAgent

**An AI-powered assistant for spike sorting and neural data analysis**

[![GitHub stars](https://img.shields.io/github/stars/arnaumarin/SpikeAgent)](https://github.com/arnaumarin/SpikeAgent/stargazers)

SpikeAgent is a web-based AI assistant that streamlines the spike sorting pipeline — from raw neural recordings to curated spike trains. It integrates with [SpikeInterface](https://github.com/SpikeInterface/spikeinterface) and leverages large language models (OpenAI, Anthropic, Google Gemini) to automate spike sorting, quality control, and data curation.

---

## Installation

### Requirements

- **Python 3.11+** (recommended via [conda](https://docs.conda.io/en/latest/miniconda.html))
- **At least one API key** from [OpenAI](https://platform.openai.com/api-keys), [Anthropic](https://console.anthropic.com/), or [Google](https://makersuite.google.com/app/apikey)

### Option 1: Install from source (recommended)

```bash
git clone https://github.com/arnaumarin/SpikeAgent.git
cd SpikeAgent
conda create -n spikeagent python=3.11 -y
conda activate spikeagent
pip install -e .
```

### Option 2: Docker

```bash
# Pull the image
docker pull ghcr.io/arnaumarin/spikeagent-cpu:latest

# Run (mount your data directories as needed)
docker run --rm -p 8501:8501 --env-file .env \
  -v /path/to/your/data:/path/to/your/data \
  ghcr.io/arnaumarin/spikeagent-cpu:latest
```

For GPU support (required for Kilosort4):

```bash
docker build -f dockerfiles/Dockerfile.gpu -t spikeagent:gpu .
docker run --rm --gpus all -p 8501:8501 --env-file .env spikeagent:gpu
```

---

## Usage

### 1. Configure API keys

Create a `.env` file in the project root with at least one key:

```bash
OPENAI_API_KEY=sk-...
# and/or
ANTHROPIC_API_KEY=sk-ant-...
# and/or
GOOGLE_API_KEY=...
```

### 2. Launch the application

```bash
conda activate spikeagent
spikeagent
```

The app will open in your browser at **http://localhost:8501**.

---

## Tutorials

The `tutorials/` directory contains Jupyter notebooks demonstrating key workflows:

- **`vlm_noise_rejection_tutorial.ipynb`** — AI-assisted spike curation using vision-language models (classifying units, quality control via waveforms and autocorrelograms)
- **`vlm_merge_simple_tutorial.ipynb`** — Automated merge analysis using crosscorrelograms, amplitude distributions, and PCA clustering

---

## Open Source Neural Data

SpikeAgent can be tested with publicly available datasets:

- [Neuropixels 2.0 chronic recordings in mice](https://doi.org/10.5522/04/24411841.v1)
- [AutoSort flexible electrode recordings](https://github.com/LiuLab-Bioelectronics-Harvard/AutoSort)

---

## Citation

If you use SpikeAgent in your work, please cite:

> Lin, Z., Marin-Llobet, A., Baek, J., He, Y., Lee, J., Wang, W., ... & Liu, J. (2025). Spike sorting AI agent. *Preprint at bioRxiv*. https://doi.org/10.1101/2025.02.11.637754

> Buccino, A. P., Hurwitz, C. L., Garcia, S., Magland, J., Siegle, J. H., Hurwitz, R., & Hennig, M. H. (2020). SpikeInterface, a unified framework for spike sorting. *eLife*, 9, e61834.

---

## License

MIT
