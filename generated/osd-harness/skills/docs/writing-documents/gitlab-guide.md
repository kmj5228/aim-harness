# OSD PR Writing Guide

## Core Sections

- Purpose
- Change Summary
- Verification
- Follow-up Documents

## OSD Rules

- PR terminology를 일관되게 쓴다
- touched module을 명시한다
- runtime code 변경과 `dist/` operational flow 변경을 구분한다
- `make`, `make -C test`, `test/run_coverage.sh`가 증명하는 범위를 넘어서서 검증을 주장하지 않는다
