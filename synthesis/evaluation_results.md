# A/B Evaluation Results: Baseline vs. Skilled Asset Selection

This report captures the results of the A/B evaluation test comparing a baseline (unskilled) LLM's visual asset suggestions against a skilled LLM utilizing the synthesized rules from `asset_selection_skill.md` and `asset_sourcing_skill.md`.

## Test Video Script
*   **0:00 - 0:05**: *"Graphify builds a knowledge graph of your entire codebase..."*
*   **0:05 - 0:10**: *"...so Claude Code stops re-reading your files every single session."*
*   **0:10 - 0:15**: *"The result? 71x fewer tokens, the exact same output, and you finally save your budget."*

---

## A/B Comparison

### A: Baseline Output (Unskilled)
*   **Segment 1 (0:00 - 0:05)**:
    *   A dynamic, dark-themed 3D network/graph animation showing node structures representing files and directories connecting via glowing links.
    *   A sleek, minimal overlay badge or text banner showing "Graphify" with a subtle neon glow effect.
*   **Segment 2 (0:05 - 0:10)**:
    *   A split-screen comparison: one panel showing a red, infinite scanning/loading cycle labeled "Re-reading files every session", the other showing a green cached checkmark indicating instant graph querying.
    *   Interactive terminal element animation where file read requests are intercepted and loaded instantly from the graph.
*   **Segment 3 (0:10 - 0:15)**:
    *   A bold, high-contrast numeric display counting down/scaling down to "71x Fewer Tokens" with a shrinking pile of token cards.
    *   Side-by-side terminal panels displaying identical output text, alongside a budget meter displaying cost savings transitioning from red to green.

### B: Skilled Output (With Selection & Sourcing Skills)
*   **Segment 1 (0:00 - 0:05)**:
    *   **Suggested Assets**: A dark-mode CLI terminal window showing the active command `graphify index ./src` running, layered beneath a floating, interactive node-link knowledge graph showing codebase file dependencies (using high-contrast cyan/purple neon nodes).
    *   **Rules Applied**: *Asset Selection Rule 1* (Concrete Visual Anchors over Generic Stock B-Roll) and *Asset Sourcing Rule 3* (Show Active CLI Terminal / Software UI Sourcing). Avoided generic coding B-roll; used direct UI/CLI execution capture. Also applied *Asset Sourcing Rule 4* (Multi-Layer Separation Asset Preparation) to place the CLI window and the node-link graph on distinct depth layers for 3D camera drift.
*   **Segment 2 (0:05 - 0:10)**:
    *   **Suggested Assets**: A screen recording of the Claude Code terminal repeatedly displaying `"...reading 148 files..."` context loading loops, framed in an apricot/clay styled console box (Claude's brand palette), floating over a blurred, dark background of file directories.
    *   **Rules Applied**: *Asset Selection Rule 2 & Rule 3* (Brand-Congruent Palettes and Visual Themes). Used actual product interface screenshots/footage framed in brand-congruent colors to provide direct technical proof. Applied drop-shadow overlays to draw attention to the repetition pain-point.
*   **Segment 3 (0:10 - 0:15)**:
    *   **Suggested Assets**: A large, bold foreground typographic overlay of "**71x**" in neon green, floating over a side-by-side comparison bar chart showing massive token reduction (e.g. 150k vs 2k tokens) and a mock API invoice highlighting budget savings.
    *   **Rules Applied**: *Asset Selection Rule 2* (Embedded First-Party / Third-Party Evidence). Used actual data proof (token numbers/bills) rather than vague stock charts. Split text and comparative charts into distinct, layered graphics using visual scale and color contrast (neon green vs. muted charcoal).

---

## Evaluation Summary & Decision

*   **Audience Context**: Serious developers ready to learn actual production work.
*   **Analysis**: The baseline suggestions rely heavily on metaphorical stock-style animations (e.g., "shrinking pile of token cards," generic "3D network/graph animation"). The skilled version grounds every segment in direct, verifiable technical evidence (active terminal commands, Claude's specific console colors, and explicit token comparison metrics).
*   **Conclusion**: The skilled version provides the required high-fidelity visual proof, drastically reducing generic visual "slop" and maintaining credibility for a developer audience.
