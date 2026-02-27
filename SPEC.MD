# Mcharts Specification (Monkey Charts)

## Project Overview
Mcharts is a simple web application for creating and viewing "Monkey Charts" — a musical chart format where lyrics are placed in a left column and chords are placed in a right column. The focus is on quick entry, easy editing, and clean PDF output.

## Target Audience
Musicians and songwriters who need a fast way to create readable lead sheets with lyrics and chords side-by-side.

## Key Features
- **Quick Entry & Editing**: Simple text-based interface for entering lyrics and chords.
- **Monkey Chart Layout**: Two-column format with lyrics on the left and chords on the right.
- **PDF Export**: Clean, well-aligned PDF output that exactly matches the rendered HTML.
- **JSON Persistence**: Support for saving and loading charts (text + settings) in JSON format.
- **Per-Chart Settings**:
    - Title
    - Left Column (Lyrics) Font Size
    - Right Column (Chords) Font Size
    - Relative Width of the Left (Chord) Column (Note: User mentioned "relative width of the left (chord) column" but previously said "chords on the right, lyrics on the left". I will assume the setting controls the left column width regardless of content type, or clarify if needed).

## User Interface (UI)
The UI follows the aesthetic and layout of `rpstory`:
- **Header**:
    - App Name: **MCharts**
    - Version Number
    - Link to Source Code
    - Entry fields for settings: Left Font Size, Right Font Size, Column Width.
- **Main Area**: Interactive editor for entering lyrics and chords.
- **Footer (Left-Aligned)**:
    - **New** button
    - **Export** button
    - **Import** button

## Technical Stack
- **Frontend**: HTML5, Vanilla CSS, Vanilla JavaScript (matching `rpstory` pattern).
- **Data Format**: JSON (for storing chart text and settings).
- **PDF Generation**: Standard browser print-to-PDF or a lightweight library if needed for perfect alignment.

## Data Requirements
- JSON schema for saving/loading charts.
