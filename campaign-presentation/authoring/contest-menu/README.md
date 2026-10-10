# Practice menu topics

The labels in labels.json replace internal IR reference codes in the practice catalog. Each topic points to the unchanged approved setup, retort and recap. Run `python3 export.py` from this directory to update source/assets/resources/242.text.bin, then update its resource inventory and coverage pins after review.

The existing SCI setup-label buffers hold four words: seven ASCII data bytes and a terminating NUL. The exporter enforces that limit and the identity of every menu command and approved retort preceding the topics. Longer labels require a separate review of the SCI buffers and their validation; changing the text resource alone would overflow them.
