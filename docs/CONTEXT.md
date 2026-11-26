# NodeBase — Cursor Context Brief

## Who I am
Non-technical founder. I use GitHub Desktop to commit and push.
Cloudflare auto-deploys on merge to main.
I do not run terminal commands.
I edit files in Cursor, save with Cmd+S, then commit via GitHub Desktop.

## How Cursor should behave
Act as a senior full-stack web developer and UX engineer.
- Make decisions a senior developer would make — do not ask
  obvious clarifying questions
- If a request would break something, say so before doing it
- Prefer clean minimal solutions over clever ones
- Write production-quality HTML and CSS
- All edits must work at 375px (mobile) and 1200px (desktop)
- ZH pages always mirror EN pages — quotes stay in English,
  UI labels translate to Hong Kong Traditional Chinese (Cantonese)

## What NodeBase is
A curatorial-identity layer for café-hoppers in Hong Kong.
NOT a directory, CRM, loyalty platform, or review site.
Curators (recommenders) are the primary unit. Cafés are evidence
of their taste. Comparable to Goodreads/Untappd, not Yelp.

## File structure
production/v2.2/ is the web root served by Cloudflare
  cafe-hoppers.html / cafe-hoppers-zh.html — main curator page
  cafe-owners.html / cafe-owners-zh.html — café owner page
  styles.css — shared stylesheet for all pages
  script.js — shared JavaScript, handles nav and scroll
  assets/images/ — all images live here

## CSS rules
- Prefer page-specific <style> blocks over editing styles.css
- Only modify styles.css if a change must apply site-wide
- Never modify script.js
- IMPORTANT: .content-block p:not(.lead-text) in styles.css
  sets color:#4a4a4a on all <p> tags inside .content-block
  Always use <div> not <p> for custom-coloured text inside
  .content-block to avoid this override

## Design tokens
Gold accent:    #C9A962 / #C8956C
Section rule:   #C8956C (3px, 48px wide, border-radius 2px)
Dark bg:        #1A1A1A
Warm beige:     #F5F0E8
Light warm:     #F7F4F0 / #F8F7F4
Card border:    #E0DBD4
Text primary:   #1A1A1A
Text secondary: #3D3D3D / #4A4A4A
Serif font:     Georgia (headings)
Sans font:      Inter (loaded via Google Fonts — already in
                cafe-hoppers.html head, add to other pages
                if not present)

## Commit workflow
After every edit: Cmd+S → GitHub Desktop → commit → push →
merge PR to main → Cloudflare deploys automatically

## Standard Cursor prompt rules
Every prompt should end with these checks:
- No terminal commands run
- No new files created unless explicitly requested
- GA4 script tags in <head> unchanged
- Header, nav, footer links unchanged
- Cmd+S to save

## Usage
Begin every Cursor prompt with: `Read CONTEXT.md first, then:`
This file gives Cursor the CSS rule, design tokens, file structure,
role definition, and NodeBase positioning without re-explaining
every session.
