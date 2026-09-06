# github_profile_banner.py
# Phase 1 source-of-truth notes:
# - Source: home-banner-logo.jpeg
# - 300x340 crop, head + shoulders
# - autocontrast(cutoff=1), contrast 1.3x, UnsharpMask(radius=3, percent=140)
# - 1-bit Floyd-Steinberg serpentine dithering
# - dark mode subject segmentation; light mode retains background
# - SVG dots are path runs with shape-rendering="crispEdges"
# - 60 scattered intro groups; no spatial wipe
# - NO LOGO 1, NO LOGO 2, NO LOGO 3
# - portrait + system-info banner: 1180x610
#
# The .npy arrays are retained as source data alongside the SVGs.
