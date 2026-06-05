# Mistakes & Learnings

- What Failed:      UnknownContentCollectionError: Unexpected error while rendering -> [newly-generated-slug]
- Why It Failed:    The Astro dev server was running before the blog posts were batch-generated, causing the Astro Content Layer's `astro:content-module-imports` virtual module to hold stale/out-of-sync references and fail during dynamic imports.
- How to Prevent:   Restart the Astro development server or clear the `.astro` cache folder when content files are batch-generated or added while the server is running.
- Scope:            global
