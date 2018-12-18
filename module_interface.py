import noise_removal as nr
import skew_correction as sc
import line_detector as ldr
import word_detector as wdr
import character_detector as chardet
import pre_recognition_processing as prp
import character_recognition as recognise
import text_generator as tg
import output_file_opener as opf
noise_removed_image = nr.image_noise_removal(r'your directory here')
skew_corrected = sc.skew_corrector(noise_removed_image)
lines = ldr.line_extractor(skew_corrected)
words = wdr.word_extractor(lines)
segmented_characters = chardet.character_detector(words)
test_data = prp.pre_recognition(segmented_characters)
prediction_matrix = recognise.character_prediction(test_data)
fileName = tg.text_generation(segmented_characters,prediction_matrix)
opf.open_file(fileName)































































































