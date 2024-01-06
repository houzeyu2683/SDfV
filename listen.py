import whisper

model = whisper.load_model("base")
result = model.transcribe("【數位主播午報】/3eNWf7Lz-qM/3eNWf7Lz-qM_0_26.mp4",language='zh')
print(result["text"])
result = model.transcribe("【數位主播午報】/KC14aynJ8kM/KC14aynJ8kM_0_2/KC14aynJ8kM_0_2_1.mp4",language='zh')
print(result["text"])
result = model.transcribe("【數位主播午報】/KC14aynJ8kM/KC14aynJ8kM_0_2.mp4",language='zh')
print(result["text"])
