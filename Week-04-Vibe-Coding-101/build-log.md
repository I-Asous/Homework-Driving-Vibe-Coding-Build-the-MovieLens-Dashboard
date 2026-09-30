# Build Log

## Moment 1: Build the required visualizations

**Prompt:** "complete task 1"

**AI's first result:** Created a Streamlit dashboard with genre counts, average rating by genre, average rating by release year, and top-five movies at rating-count floors of 50 and 150. Added a genre multi-select and a minimum-rating selector.

**What changed and why:** Testing exposed two issues: selecting multiple genres could duplicate movie ratings in the release-year calculation, and Streamlit reported duplicate chart IDs for the two top-movie comparisons. Changed the year filter to include a movie's rating once if it matches any selected genre, then assigned unique keys to the comparison charts. Also replaced the deprecated chart-width argument. The default and filtered app-test runs then passed.

## Moment 2: Identify the remaining assignment work

**Prompt:** "whats next to do"

**AI's first result:** Identified the build log, pushing the app and data to a public GitHub repository, deploying through Streamlit Community Cloud, testing the public URL in a private window, and submitting that URL.

**What changed and why:** No dashboard code changed. I chose the build log as the next step and recorded these actual prompt and revision details here.
