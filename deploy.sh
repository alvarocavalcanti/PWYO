#!/bin/sh

cp pwyo.py .git/hooks/
rm .git/hooks/pre-commit
mv .git/hooks/pwyo.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit