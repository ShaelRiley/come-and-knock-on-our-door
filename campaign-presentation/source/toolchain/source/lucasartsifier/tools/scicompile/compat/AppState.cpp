// CaKoOD distribution notice added 2026-10-06: this is part of the modified
// Linux headless SCICompanion port, licensed GPL-2.0-or-later. The inherited
// port/local changes were preserved on this date; their original change dates
// are not established here. Only this notice was added for this distribution.
// See ../../../MODIFIED-SOURCE-PROVENANCE.json (from compat/ or patched/) for exact
// pre-notice hashes and upstream-file comparisons. Historical comments below
// describe earlier work and do not supersede that exact provenance record.
#include "stdafx.h"
#include "AppState.h"

// The single global instance the entire compiler subsystem talks to.
AppState *appState = nullptr;

AppState::AppState()
{
    // Order matters: the class browser needs the dependency tracker; the resource
    // map needs this object (as ISCIAppServices) and the recency tracker.
    _dependencyTracker = std::make_unique<DependencyTracker>(FALSE /*fTrackHeaderFiles*/);
    _resourceMap = std::make_unique<CResourceMap>(this, &_resourceRecency);
    _classBrowser = std::make_unique<SCIClassBrowser>(*_dependencyTracker);
}

AppState::~AppState()
{
    // Tear down the class browser first: it owns a background scheduler thread
    // that must be joined before the objects it references disappear.
    if (_classBrowser)
    {
        _classBrowser->ExitSchedulerAndReset();
    }
    _classBrowser.reset();
    _resourceMap.reset();
    _dependencyTracker.reset();
}

void AppState::LogInfo(const TCHAR *pszFormat, ...)
{
    va_list args;
    va_start(args, pszFormat);
    vfprintf(stderr, pszFormat, args);
    va_end(args);
    fputc('\n', stderr);
}
