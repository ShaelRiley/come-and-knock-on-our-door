#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
port=../vendor/lucasartsifier
test "$(git -C "$port" rev-parse HEAD)" = 45068351290ffd90e74186c69322d200fa60cafd
test "$(git -C "$port/vendor/SCICompanion" rev-parse HEAD)" = f1a603b48b1aa7abf94f78574a8f69a653e2ca62
test "$(sha256sum "$port/tools/scicompile/build/scicompile" | cut -d' ' -f1)" = 608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e
mkdir -p build/compiled evidence
python3 compose.py
python3 ../../tools/check_sci_conditionals.py src > evidence/boolean-source-audit.log
find src -maxdepth 1 -name '*.sco' -delete
python3 prepare.py seed
for entry in 980:module980 981:module981 982:module982 983:module983 984:module984 985:module985 986:module986 987:module987 988:module988 989:module989 990:module990 991:module991 997:module997 0:main; do
 number=${entry%%:*};name=${entry#*:}
 "$port/tools/scicompile/build/scicompile" --version sci11 "$PWD" "$PWD/src/$name.sc" "$PWD/build/compiled/$number.scr.bin" > "evidence/compile-$name.log" 2>&1 || { cat "evidence/compile-$name.log";exit 1; }
 tail -2 "evidence/compile-$name.log"
 if grep -q '\[error\]' "evidence/compile-$name.log";then exit 1;fi
done
python3 prepare.py package
