// CaKoOD distribution notice added 2026-10-06: this is part of the modified
// Linux headless SCICompanion port, licensed GPL-2.0-or-later. The inherited
// port/local changes were preserved on this date; their original change dates
// are not established here. Only this notice was added for this distribution.
// See ../../../MODIFIED-SOURCE-PROVENANCE.json (from compat/ or patched/) for exact
// pre-notice hashes and upstream-file comparisons. Historical comments below
// describe earlier work and do not supersede that exact provenance record.
// See CMake/BUILD_NOTES: the SCI parser-combinator headers are template-heavy
// and, under MSVC's non-conformant two-phase lookup, resolved sci:: / std:: /
// parser-global names at instantiation. GCC resolves non-dependent names at
// definition, so we establish the expected context first.
#pragma once
#include "ScriptOM.h"     // full sci::Comment / CommentType / SyntaxNode / *Value defs
// Parser globals referenced inside templates before their in-file declaration:
int charToI(char ch);
extern char const errIntegerTooLarge[];
extern char const errIntegerTooSmall[];
using namespace sci;
using namespace std;
