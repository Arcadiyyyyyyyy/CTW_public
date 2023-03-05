#!/bin/bash
echo 'Starting Up'
python criticlworkparse.py &
streamlit run Home.py &
wait