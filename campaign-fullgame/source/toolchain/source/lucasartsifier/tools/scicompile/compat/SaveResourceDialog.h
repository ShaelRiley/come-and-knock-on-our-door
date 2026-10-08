// CaKoOD distribution notice added 2026-10-06: this is part of the modified
// Linux headless SCICompanion port, licensed GPL-2.0-or-later. The inherited
// port/local changes were preserved on this date; their original change dates
// are not established here. Only this notice was added for this distribution.
// See ../../../MODIFIED-SOURCE-PROVENANCE.json (from compat/ or patched/) for exact
// pre-notice hashes and upstream-file comparisons. Historical comments below
// describe earlier work and do not supersede that exact provenance record.
#pragma once
// Headless stub: ResourceMap.cpp's AppendResourceAskForNumber uses this dialog,
// but the headless compiler only calls AppendResource(...) directly. DoModal()
// returns IDCANCEL so that code path is inert.
#include <string>
enum class ResourceType;
class CWnd;
class SaveResourceDialog
{
public:
    SaveResourceDialog(bool /*warnOnOverwrite*/, ResourceType /*type*/, CWnd * /*parent*/ = nullptr) {}
    void Init(int, int, const std::string & = std::string()) {}
    int  DoModal() { return 2; /* IDCANCEL */ }
    int  GetResourceNumber() { return 0; }
    int  GetPackageNumber() { return 0; }
    std::string GetName() { return std::string(); }
};
