#!/bin/bash
cat links.txt | xargs -I % wget -P data/ %
