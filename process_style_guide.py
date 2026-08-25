#!/usr/bin/env python3
"""Post-process apple-style-guide.md:
1. Promote known section headings to #/##/### (using TOC as reference)
2. Convert "•" bullets to Markdown "-"
3. Strip repeated "Apple Style Guide N" page-footer lines
"""
import re
import sys

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # --- Define headings from the TOC ---
    h1_headings = {
        'About this guide',
        'Style and usage A–Z',
        'Writing inclusively',
        'Units of measure',
        'Technical notation',
        'International style',
        'Copyright and trademarks',
    }

    h2_headings = {
        'About the guide',
        'Changes to the guide',
        'Numbers',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'Intro to inclusive writing',
        'General guidelines',
        'Inclusive representation',
        'Gender identity',
        'Writing about disability',
        'Intro to units of measure',
        'Prefixes for units of measure',
        'Names and unit symbols for units of measure',
        'Intro to technical notation',
        'Code',
        'Syntax descriptions',
        'Code font in text',
        'Placeholder names in text',
        'Intro to international style',
        'Countries',
        'Currency',
        'Dates and times',
        'Decimals',
        'Languages',
        'Telephone numbers',
    }

    # Track state
    in_toc = False
    units_of_measure_seen_h1 = False
    output = []
    first_line_processed = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # --- Skip the TOC section (from "Contents" through last TOC entry) ---
        if stripped == 'Contents':
            in_toc = True
            continue

        if in_toc:
            # TOC entries have page numbers: "About this guide 4"
            # They won't exactly match our heading names (which lack numbers)
            # End of TOC = first line that exactly matches a heading
            if stripped in h1_headings or stripped in h2_headings:
                in_toc = False
                # fall through to process this line normally
            else:
                # Also skip "Apple Style Guide N" lines that appear in TOC
                if re.match(r'^Apple Style Guide \d+$', stripped):
                    continue
                # Skip any other TOC line (has page number suffix)
                continue

        # --- Remove "Apple Style Guide N" footer lines ---
        if re.match(r'^Apple Style Guide \d+$', stripped):
            continue

        # --- Handle the document title ---
        if stripped == 'Apple Style Guide' and not first_line_processed:
            output.append('# Apple Style Guide')
            first_line_processed = True
            continue

        # --- Convert "•" bullets to "-" ---
        if stripped.startswith('•'):
            indent = len(line) - len(line.lstrip())
            new_line = re.sub(r'^•\s*', '', stripped)
            output.append(' ' * indent + '- ' + new_line)
            continue

        # --- Promote headings ---
        if stripped in h1_headings:
            if stripped == 'Units of measure' and units_of_measure_seen_h1:
                # Second occurrence is under "International style" → ##
                output.append(f'## {stripped}')
            else:
                if stripped == 'Units of measure':
                    units_of_measure_seen_h1 = True
                output.append(f'# {stripped}')
            continue

        if stripped in h2_headings:
            output.append(f'## {stripped}')
            continue

        # --- Normal line ---
        output.append(line.rstrip('\n'))

    result = '\n'.join(output)

    # Clean up: collapse 3+ blank lines to 2
    result = re.sub(r'\n{3,}', '\n\n', result)

    # Strip trailing whitespace on each line
    result = '\n'.join(line.rstrip() for line in result.split('\n'))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result + '\n')

    print(f"Done. Wrote {output_path}")

if __name__ == '__main__':
    src = 'apple-style-guide.md'
    dst = 'apple-style-guide.md'
    process_file(src, dst)
