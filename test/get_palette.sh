#!/bin/bash

curl -X POST localhost:8000/palette -F "image=@./test/test-image.jpg"