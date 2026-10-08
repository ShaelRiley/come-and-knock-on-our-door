// CaKoOD distribution notice added 2026-10-06: this is part of the modified
// Linux headless SCICompanion port, licensed GPL-2.0-or-later. The inherited
// port/local changes were preserved on this date; their original change dates
// are not established here. Only this notice was added for this distribution.
// See ../../../MODIFIED-SOURCE-PROVENANCE.json (from compat/ or patched/) for exact
// pre-notice hashes and upstream-file comparisons. Historical comments below
// describe earlier work and do not supersede that exact provenance record.
// Link stubs for symbols whose defining vendor file is NOT compiled headless.
// SniffSCIVersion lives in VersionDetectionHelper.cpp (heavy resource enumeration,
// many MSVC rvalue-binding sites). The headless driver skips version sniffing and
// pins the SCI version explicitly (SkipNextVersionSniff + SetVersion), so this is
// never actually invoked.
#include "stdafx.h"
#include "GameFolderHelper.h"

void SniffSCIVersion(GameFolderHelper &helper)
{
    // No-op: version is set explicitly by the compile driver.
    (void)helper;
}
