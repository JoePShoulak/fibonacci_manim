Q=ql

FOLDER = 480p15
ifeq ($(Q),qm)
	FOLDER = 720p30
endif
ifeq ($(Q),qh)
	FOLDER = 1080p60
endif
ifeq ($(Q),qp)
	FOLDER = 1440p60
endif
ifeq ($(Q),qk)
	FOLDER = 2160p60
endif

render:
	manim -a$(Q) scene.py

all: render export

clean:
	rm -rf ./media/videos/scene/*/partial_movie_files/

scrub: clean
	rm -rf ./media/videos/scene/*/*.mp4
	rm -rf ./media/videos/scene/*/*.srt

nuke: scrub
	rm -rf ./exports/*
	
%.txt:
	sed 's/FOLDER/$(FOLDER)/g' sceneLists/master.txt > $@

output_%.mp4: %.txt
	ffmpeg -f concat -safe 0 -y -i $< -c:v copy -c:a aac -b:a 192k -map 0:v -map 0:a? exports/output_$(Q).mp4

export: output_$(Q).mp4

.PHONY: render all clean scrub nuke export
