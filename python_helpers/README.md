Module for collecting and processing text files from a directory.  
Creates a single markdown file with sorted content.  
how to setup:
```
poetry install
```
 
## text_collector_from_tg_transcribed_voices.py
This script is just for transcriptions of voice mesages from tg, because it extracts _order_ from filename  

— we got voices from tg chat  
— transcrubed them with whisper  
— and want to collect all voices together  


### how to run:  
```
python text_collector_from_tg_transcribed_voices.py /path/to/source/directory /path/to/output/file.md
```  
  
### the result:  
``` 
# filename_1  
transcribed voice message  
 
# filename_2  
transcribed voice message  
```