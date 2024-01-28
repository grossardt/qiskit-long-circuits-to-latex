# Copyright Andre Grossardt 2022-2024
# Licensed under the MIT license, see LICENSE.txt for details

.PHONY: test

all_check: test

test:
	python -m unittest discover -v test