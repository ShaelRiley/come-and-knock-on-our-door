// CaKoOD distribution notice added 2026-10-06: this is part of the modified
// Linux headless SCICompanion port, licensed GPL-2.0-or-later. The inherited
// port/local changes were preserved on this date; their original change dates
// are not established here. Only this notice was added for this distribution.
// See ../../../MODIFIED-SOURCE-PROVENANCE.json (from compat/ or patched/) for exact
// pre-notice hashes and upstream-file comparisons. Historical comments below
// describe earlier work and do not supersede that exact provenance record.
#pragma once
// Headless stub (ResourceMapOperations.cpp DeleteResource path; not compile-path).
class CRemoveScriptDialog
{
public:
    CRemoveScriptDialog(unsigned short = 0) {}
    int  DoModal() { return 2; /* IDCANCEL */ }
    bool AlsoDelete() { return false; }
};
