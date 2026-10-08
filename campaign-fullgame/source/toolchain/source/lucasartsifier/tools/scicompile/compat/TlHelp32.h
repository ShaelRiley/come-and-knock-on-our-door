// CaKoOD distribution notice added 2026-10-06: this is part of the modified
// Linux headless SCICompanion port, licensed GPL-2.0-or-later. The inherited
// port/local changes were preserved on this date; their original change dates
// are not established here. Only this notice was added for this distribution.
// See ../../../MODIFIED-SOURCE-PROVENANCE.json (from compat/ or patched/) for exact
// pre-notice hashes and upstream-file comparisons. Historical comments below
// describe earlier work and do not supersede that exact provenance record.
// Toolhelp process-snapshot API stub. Referenced only by util.cpp's
// TerminateProcessTree(), which is never called in the headless compiler.
#pragma once
#include "winshim.h"

typedef struct tagPROCESSENTRY32
{
    DWORD     dwSize;
    DWORD     cntUsage;
    DWORD     th32ProcessID;
    ULONG_PTR th32DefaultHeapID;
    DWORD     th32ModuleID;
    DWORD     cntThreads;
    DWORD     th32ParentProcessID;
    LONG      pcPriClassBase;
    DWORD     dwFlags;
    char      szExeFile[260];
} PROCESSENTRY32;

inline HANDLE CreateToolhelp32Snapshot(DWORD, DWORD) { return INVALID_HANDLE_VALUE; }
inline int    Process32First(HANDLE, PROCESSENTRY32 *) { return 0; }
inline int    Process32Next(HANDLE, PROCESSENTRY32 *) { return 0; }
