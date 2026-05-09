# Content Creation Automation Pipeline

> **⚠️ DISCLAIMER:** This project is a **working prototype ("brouillon")** and is highly **specific** to a particular environment and workflow. It was developed for personal use and is shared here for inspiration, reference, or adaptation. Expect hardcoded paths, specific folder structures, and a "raw" coding style.

## 📌 Overview

This project is an end-to-end automated pipeline designed to create and publish short-form video content (TikToks, Instagram Reels, YouTube Shorts). It leverages AI for scriptwriting and metadata, Remotion for programmatic video editing, and Telegram for final delivery.

## 🏗️ Architecture & Workflow

The pipeline is orchestrated by a main shell script (`automate.sh`) that connects several specialized modules:

1.  **Script Generation (`creator/`):** Uses the Google Gemini API to generate scripts based on specific "angles" (e.g., Stoic, Cynical, Wise) and themes.
2.  **Asset Selection (`selector/`):** Python scripts that select appropriate video backgrounds and assets based on the content type.
3.  **Video Assembly (`assembler/`):** A Remotion project that renders the base video by sequencing selected clips and adding background audio.
4.  **Transcription & Subtitles (`captioner/`):**
    * Uses Whisper (via Node.js) to transcribe the generated audio.
    * A second Remotion project applies styled, animated subtitles to the video.
5.  **Metadata & Thumbnail (`deliver/`):**
    * **AI Metadata:** Gemini extracts the best hook for the description and selects relevant hashtags.
    * **Dynamic Thumbnails:** Python (Pillow) generates a custom thumbnail image with high-CTR text overlays.
6.  **Delivery (`deliver/`):** Automatically sends the final MP4, description, and thumbnail to a designated Telegram chat via a Bot.

## 🚀 Key Features

* **Multi-Character Templates:** Supports different visual/audio styles like "Default", "Oogway" (Wise), or "Joker" (Dark/Cynical).
* **AI-Powered Copywriting:** Automatic generation of hooks, descriptions, and hashtags.
* **Dynamic Video Rendering:** Programmatic editing via Remotion (React-based).
* **Automated Triggers:** Includes scripts for daily automated runs with rotating themes.
* **Telegram Integration:** Immediate notification and file delivery upon completion.

## 🛠️ Prerequisites

To run this pipeline, you will need:

* **Node.js & npm** (for Remotion and Whisper scripts)
* **Python 3.10+** (for AI logic and image processing)
    * see requirements.txt
* **FFmpeg** (essential for Remotion and audio processing)
* **yt-dlp** (for downloading audio assets)
* **API Keys:**
    * Google Gemini API Key
    * Telegram Bot Token

## ⚙️ Setup & Configuration

1.  **Environment Variables:**
    Create a `.env` file in the root directory. Use the provided code structure as a reference for required variables:
    * `GEMINI_API_KEY`: Your Google AI Studio key.
    * `TOKEN`: Your Telegram Bot token.
    * `URL`: Your Telegram Bot API URL (or standard API).
    * `PYTHON_PATH`, `YT_DLP_PATH`, etc.: Paths to your local executables.
    * `PROJECT_BASE_PATH`: The absolute path to the project root.
    * **Cf .env.bak** for other needed variables

2.  **Dependencies:**
    ```bash
    # Install Python deps
    pip install google-genai requests python-dotenv Pillow

    # Install Node.js deps in assembler and captioner folders
    cd assembler && npm install
    cd ../captioner && npm install
    ```

## 📂 Project Structure

* `automate.sh`: The main entry point script.
* `assembler/`: Remotion source code for the raw video composition.
* `captioner/`: Remotion source code for subtitling logic.
* `creator/`: Python logic for Gemini-powered scriptwriting.
* `deliver/`: Python scripts for thumbnail generation and Telegram uploading.
* `selector/`: Logic for picking video background clips.
* `trigger/`: Daily automation triggers and theme pools.

## ⚠️ Important Notes

* **Hardcoded Paths:** Many scripts rely on environment variables pointing to specific local directories. Ensure your `.env` is perfectly configured.
* **Specific Assets:** The project expects certain font files (e.g., `Lora-SemiBold.ttf`) and template images to exist in the `deliver/` and `captioner/public/` folders.
* **Customization:** You will likely need to modify the `system_instruction` in `script-creator.py` and the prompts in `deliver.py` to match your specific niche.
* **Local ressources**: this pipeline relies on several local ressources such as videos sources, audio etc... You can see an example of the local tree files in the `tree.txt` file.
