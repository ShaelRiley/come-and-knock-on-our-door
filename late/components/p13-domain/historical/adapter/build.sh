#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
port=../vendor/lucasartsifier
upstream="$port/vendor/SCICompanion"
test "$(git -C "$port" rev-parse HEAD)" = 45068351290ffd90e74186c69322d200fa60cafd
test "$(git -C "$upstream" rev-parse HEAD)" = f1a603b48b1aa7abf94f78574a8f69a653e2ca62
mkdir -p build/compiled evidence
python3 generate.py
python3 ../../tools/check_sci_conditionals.py src/module995.sc src/main.sc src/methods.sc.in > evidence/conditional-gate.log
cat evidence/conditional-gate.log
python3 prepare.py seed
for entry in 995:module995 0:main; do
    number=${entry%%:*}; name=${entry#*:}
    "$port/tools/scicompile/build/scicompile" --version sci11 "$PWD" "$PWD/src/$name.sc" "$PWD/build/compiled/$number.scr.bin" > "evidence/compile-$name.log" 2>&1 || { cat "evidence/compile-$name.log"; exit 1; }
    cat "evidence/compile-$name.log"
    if grep -q '\[error\]' "evidence/compile-$name.log"; then exit 1; fi
done
python3 prepare.py package
python3 validate.py
python3 -m unittest discover -s tests -v > evidence/source-tests.log 2>&1 || { cat evidence/source-tests.log; exit 1; }
cat evidence/source-tests.log
sha256sum README.md build.sh game.ini src/*.sc src/*.in src/*.sco tests/*.py *.py manifest.json selectors.json object-bindings.json build/compiled/* > evidence/build-sha256.txt
