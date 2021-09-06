#!/usr/bin/env bash

cd $(dirname $0)

rm body.md

for i in {1..7}; do
  echo "" >> body.md
  cat "../exercise_0${i}/instructions.md" >> body.md
  echo "" >> body.md
done

pandoc main.md body.md -o VUnit_Tutorial.pdf --from markdown --template ./eisvogel.latex --listings -N --top-level-division=chapter

